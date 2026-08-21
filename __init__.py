"""Hanzi Kanji Cross-Reference Add-on for Anki."""
from aqt import mw, gui_hooks
from .backend import ConfigManager, LookupEngine, BridgeManager

config_manager = ConfigManager(mw)
lookup_engine = LookupEngine()
bridge_manager = BridgeManager(lookup_engine, config_manager)

# Register hooks for webview content injection and JS messaging
gui_hooks.webview_will_set_content.append(bridge_manager.inject_assets)
gui_hooks.webview_did_receive_js_message.append(bridge_manager.on_js_message)
