"""Unit tests for lookup engine and variant mapping provider."""
import sys
import unittest
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

from backend.engine import LookupEngine
from backend.providers.variant_provider import VariantMappingProvider
from backend.constants import (
    ROOT_DIR,
    DATA_DIR,
    UI_DIR,
    DATASET_PATH,
    TOOLTIP_CSS_PATH,
    TOOLTIP_JS_PATH,
    ADDON_NAME,
    BRIDGE_PREFIX,
    DEFAULT_CONFIG,
)


class TestConstants(unittest.TestCase):

    def test_paths_exist(self):
        self.assertTrue(ROOT_DIR.exists(), f"ROOT_DIR does not exist: {ROOT_DIR}")
        self.assertTrue(DATA_DIR.exists(), f"DATA_DIR does not exist: {DATA_DIR}")
        self.assertTrue(UI_DIR.exists(), f"UI_DIR does not exist: {UI_DIR}")
        self.assertTrue(DATASET_PATH.exists(), f"DATASET_PATH does not exist: {DATASET_PATH}")
        self.assertTrue(TOOLTIP_CSS_PATH.exists(), f"TOOLTIP_CSS_PATH does not exist: {TOOLTIP_CSS_PATH}")
        self.assertTrue(TOOLTIP_JS_PATH.exists(), f"TOOLTIP_JS_PATH does not exist: {TOOLTIP_JS_PATH}")

    def test_addon_metadata_and_defaults(self):
        self.assertEqual(ADDON_NAME, "douji")
        self.assertEqual(BRIDGE_PREFIX, "douji:")
        self.assertIn("modifier_key", DEFAULT_CONFIG)


class TestLookupEngine(unittest.TestCase):

    def setUp(self):
        self.provider = VariantMappingProvider()
        self.engine = LookupEngine(providers=[self.provider])

    def test_all_different_characters(self):
        res = self.engine.lookup("気")
        self.assertIsNotNone(res)
        self.assertTrue(res["found"])
        self.assertEqual(res["jp"], ["気"])
        self.assertEqual(res["sc"], ["气"])
        self.assertEqual(res["tc"], ["氣"])
        self.assertTrue(res["all_different"])
        self.assertFalse(res["all_identical"])

    def test_all_identical_characters(self):
        res = self.engine.lookup("人")
        self.assertIsNotNone(res)
        self.assertTrue(res["found"])
        self.assertEqual(res["jp"], ["人"])
        self.assertEqual(res["sc"], ["人"])
        self.assertEqual(res["tc"], ["人"])
        self.assertTrue(res["all_identical"])

    def test_unmapped_character_empty_state(self):
        res = self.engine.lookup("あ")
        self.assertIsNotNone(res)
        self.assertFalse(res["found"])
        self.assertEqual(res["message"], "No character cross-reference found")


if __name__ == "__main__":
    unittest.main()
