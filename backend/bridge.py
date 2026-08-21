"""Bridge connecting Anki webview JS and Python backend."""
import json
import os
from typing import Any, Tuple, Optional
from .engine import LookupEngine
from .config import ConfigManager

PREFIX = "hanzikanji:"


class BridgeManager:
    """Handles JS messages and injects web assets into reviewer webviews."""

    def __init__(self, engine: LookupEngine, config_manager: ConfigManager):
        self.engine = engine
        self.config_manager = config_manager
        self._web_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web"
        )
        self._css_cache: Optional[str] = None
        self._js_cache: Optional[str] = None

    def _get_css(self) -> str:
        if self._css_cache is None:
            css_path = os.path.join(self._web_dir, "tooltip.css")
            if os.path.exists(css_path):
                with open(css_path, "r", encoding="utf-8") as f:
                    self._css_cache = f.read()
            else:
                self._css_cache = ""
        return self._css_cache

    def _get_js(self) -> str:
        if self._js_cache is None:
            js_path = os.path.join(self._web_dir, "tooltip.js")
            if os.path.exists(js_path):
                with open(js_path, "r", encoding="utf-8") as f:
                    self._js_cache = f.read()
            else:
                self._js_cache = ""
        return self._js_cache

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
                f"if (window.HanziKanjiBridge) {{"
                f" window.HanziKanjiBridge.onResult({result_json}, {safe_req_id});"
                f" }}"
            )

            # Evaluate callback on the webview context
            if hasattr(context, "eval"):
                context.eval(callback_script)
            elif hasattr(context, "web") and hasattr(context.web, "eval"):
                context.web.eval(callback_script)
            else:
                try:
                    from aqt import mw
                    if mw and mw.reviewer and mw.reviewer.web:
                        mw.reviewer.web.eval(callback_script)
                except Exception:
                    pass

            return (True, result)

        if subcommand.startswith("config:"):
            conf = self.config_manager.all()
            conf_json = json.dumps(conf, ensure_ascii=False)
            callback_script = (
                f"if (window.HanziKanjiBridge) {{"
                f" window.HanziKanjiBridge.onConfig({conf_json});"
                f" }}"
            )
            if hasattr(context, "eval"):
                context.eval(callback_script)
            elif hasattr(context, "web") and hasattr(context.web, "eval"):
                context.web.eval(callback_script)
            return (True, conf)

        return handled

    def inject_assets(self, web_content: Any, context: Any) -> None:
        """Inject CSS and JS into reviewer webview content."""
        is_reviewer = False
        context_name = getattr(context, "__class__", {}).__name__ if hasattr(context, "__class__") else ""
        if "Reviewer" in str(context_name) or "Reviewer" in str(type(context)):
            is_reviewer = True

        try:
            from aqt import mw
            if mw and getattr(mw, "reviewer", None) is not None:
                if context is mw.reviewer or context is getattr(mw.reviewer, "web", None):
                    is_reviewer = True
        except Exception:
            pass

        if is_reviewer:
            css = self._get_css()
            js = self._get_js()
            config_json = json.dumps(self.config_manager.all(), ensure_ascii=False)

            init_script = f"""
            <style id="hanzi-kanji-styles">
            {css}
            </style>
            <script id="hanzi-kanji-script">
            window.HANZI_KANJI_INITIAL_CONFIG = {config_json};
            {js}
            </script>
            """
            if hasattr(web_content, "head"):
                web_content.head += init_script

    def on_card_shown(self) -> None:
        """Ensure scripts are active when a card question or answer is displayed."""
        try:
            from aqt import mw
            if mw and mw.reviewer and mw.reviewer.web:
                js = self._get_js()
                css = self._get_css()
                config_json = json.dumps(self.config_manager.all(), ensure_ascii=False)
                ensure_script = (
                    f"if (!document.getElementById('hanzi-kanji-styles')) {{"
                    f"  var s = document.createElement('style');"
                    f"  s.id = 'hanzi-kanji-styles';"
                    f"  s.textContent = {json.dumps(css)};"
                    f"  document.head.appendChild(s);"
                    f"}}"
                    f"if (!window.HANZI_KANJI_INITIAL_CONFIG) {{"
                    f"  window.HANZI_KANJI_INITIAL_CONFIG = {config_json};"
                    f"}}"
                    f"{js}"
                )
                mw.reviewer.web.eval(ensure_script)
        except Exception:
            pass
