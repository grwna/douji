"""Douji (同字) - Cross-reference add-on for Anki."""
from aqt import mw, gui_hooks
from .backend import ConfigManager, LookupEngine, BridgeManager

config_manager = ConfigManager(mw)
lookup_engine = LookupEngine()
bridge_manager = BridgeManager(lookup_engine, config_manager)

# Register hooks for webview content injection and JS messaging
gui_hooks.webview_will_set_content.append(bridge_manager.inject_assets)
gui_hooks.webview_did_receive_js_message.append(bridge_manager.on_js_message)

# Fallback injection on card render to ensure script is active on all cards
gui_hooks.reviewer_did_show_question.append(lambda card: bridge_manager.on_card_shown())
gui_hooks.reviewer_did_show_answer.append(lambda card: bridge_manager.on_card_shown())
