"""Bridge connecting Anki webview JS and Python backend."""
import json
from pathlib import Path
from typing import Any, Tuple
from .engine import LookupEngine
from .config import ConfigManager

PREFIX = "douji:"


class BridgeManager:
    """Handles JS messages and injects web assets into reviewer webviews."""

    def __init__(self, engine: LookupEngine, config_manager: ConfigManager):
        self.engine = engine
        self.config_manager = config_manager
        self._web_dir = Path(__file__).resolve().parents[1] / "web"
        self._file_cache: dict[str, str] = {}

    def _read_web_file(self, filename: str) -> str:
        """Read and cache a file from the web directory."""
        if filename not in self._file_cache:
            path = self._web_dir / filename
            if path.exists():
                self._file_cache[filename] = path.read_text(encoding="utf-8")
            else:
                self._file_cache[filename] = ""
        return self._file_cache[filename]

    @staticmethod
    def _eval_js(context: Any, script: str) -> None:
        """Send JS to the webview, trying context methods then falling back to mw."""
        if hasattr(context, "eval"):
            context.eval(script)
        elif hasattr(context, "web") and hasattr(context.web, "eval"):
            context.web.eval(script)
        else:
            try:
                from aqt import mw
                if mw and mw.reviewer and mw.reviewer.web:
                    mw.reviewer.web.eval(script)
            except Exception:
                pass

    @staticmethod
    def _is_reviewer(context: Any) -> bool:
        """Check whether the webview context belongs to the Anki reviewer."""
        try:
            from aqt import mw
            if mw and getattr(mw, "reviewer", None) is not None:
                return context is mw.reviewer or context is getattr(mw.reviewer, "web", None)
        except Exception:
            pass
        return "Reviewer" in type(context).__name__

    def on_js_message(self, handled: Tuple[bool, Any], message: str, context: Any) -> Tuple[bool, Any]:
        """Process incoming bridge messages from JS."""
        if not isinstance(message, str) or not message.startswith(PREFIX):
            return handled

        subcommand = message[len(PREFIX):]

        if subcommand.startswith("lookup:"):
            payload_str = subcommand[len("lookup:"):]
            try:
                data = json.loads(payload_str)
                char = data.get("char", "")
                req_id = data.get("req_id", "")
            except Exception:
                char = payload_str
                req_id = ""

            result = self.engine.lookup(char)
            result_json = json.dumps(result, ensure_ascii=False)
            safe_req_id = json.dumps(req_id)

            callback_script = (
                f"if (window.DoujiBridge) {{"
                f" window.DoujiBridge.onResult({result_json}, {safe_req_id});"
                f" }}"
            )
            self._eval_js(context, callback_script)
            return (True, result)

        if subcommand.startswith("config:"):
            conf = self.config_manager.all()
            conf_json = json.dumps(conf, ensure_ascii=False)
            callback_script = (
                f"if (window.DoujiBridge) {{"
                f" window.DoujiBridge.onConfig({conf_json});"
                f" }}"
            )
            self._eval_js(context, callback_script)
            return (True, conf)

        return handled

    def inject_assets(self, web_content: Any, context: Any) -> None:
        """Inject CSS and JS into reviewer webview content."""
        if not self._is_reviewer(context):
            return

        css = self._read_web_file("tooltip.css")
        js = self._read_web_file("tooltip.js")
        config_json = json.dumps(self.config_manager.all(), ensure_ascii=False)

        init_script = f"""
        <style id="douji-styles">
        {css}
        </style>
        <script id="douji-script">
        window.DOUJI_INITIAL_CONFIG = {config_json};
        {js}
        </script>
        """
        if hasattr(web_content, "head"):
            web_content.head += init_script

    def on_card_shown(self) -> None:
        """Ensure scripts are active when a card question or answer is displayed.

        Only injects a lightweight bootstrap check — the full JS bundle is loaded
        once via inject_assets. This avoids re-evaluating the entire tooltip.js
        on every card flip.
        """
        try:
            from aqt import mw
            if mw and mw.reviewer and mw.reviewer.web:
                css = self._read_web_file("tooltip.css")
                config_json = json.dumps(self.config_manager.all(), ensure_ascii=False)
                ensure_script = (
                    f"if (!document.getElementById('douji-styles')) {{"
                    f"  var s = document.createElement('style');"
                    f"  s.id = 'douji-styles';"
                    f"  s.textContent = {json.dumps(css)};"
                    f"  document.head.appendChild(s);"
                    f"}}"
                    f"if (!window.DOUJI_INITIAL_CONFIG) {{"
                    f"  window.DOUJI_INITIAL_CONFIG = {config_json};"
                    f"}}"
                    f"if (!window.DoujiBridge) {{"
                    f"  {self._read_web_file('tooltip.js')}"
                    f"}}"
                )
                mw.reviewer.web.eval(ensure_script)
        except Exception:
            pass
