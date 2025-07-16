#!/usr/bin/env python3

import unittest
from parameterized import parameterized

# Assuming utils.py is in the same directory
import utils

class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any) -> None:
        """Tests utils.access_nested_map with various inputs."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

if __name__ == '__main__':
    unittest.main()
