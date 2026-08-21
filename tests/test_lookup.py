"""Unit tests for lookup engine and variant mapping provider."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.engine import LookupEngine
from backend.providers.variant_provider import VariantMappingProvider


class TestLookupEngine(unittest.TestCase):

    def setUp(self):
        data_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "char_variants.json",
        )
        self.provider = VariantMappingProvider(data_path=data_path)
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
