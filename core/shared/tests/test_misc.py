# Test Miscilaneous Utilities

from unittest import TestCase

from core.shared.utils.misc import yaml_coerce


class TestMisc(TestCase):
    # Test yaml_coerce
    def test_yaml_coerce(self):
        self.assertEqual(yaml_coerce("a"), "a")
        self.assertEqual(yaml_coerce(1), 1)
        self.assertEqual(yaml_coerce({"a": 1}), {"a": 1})
        self.assertEqual(yaml_coerce('{"a": 1}'), {"a": 1})
        self.assertRaises(ValueError, yaml_coerce, '{"a": 1')
