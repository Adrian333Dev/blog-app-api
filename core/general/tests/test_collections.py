# Test Custom Collections

from unittest import TestCase

from core.general.utils.collections import deep_update


class TestCollections(TestCase):
    # Test deep_update
    def test_deep_update(self):
        d = {"a": 1, "b": {"c": 2}}
        u = {"b": {"d": 3}}
        expected = {"a": 1, "b": {"c": 2, "d": 3}}
        self.assertEqual(deep_update(d, u), expected)

    def test_deep_update_with_list(self):
        d = {"a": 1, "b": {"c": 2}}
        u = {"b": {"d": [3, 4]}}
        expected = {"a": 1, "b": {"c": 2, "d": [3, 4]}}
        self.assertEqual(deep_update(d, u), expected)

    def test_deep_update_with_list_overwrite(self):
        d = {"a": 1, "b": {"c": 2, "d": [3, 4]}}
        u = {"b": {"d": [5, 6]}}
        expected = {"a": 1, "b": {"c": 2, "d": [5, 6]}}
        self.assertEqual(deep_update(d, u), expected)
