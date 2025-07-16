#!/usr/bin/env python3
"""Unit tests for the utils.py file.
"""
import unittest
from parameterized import parameterized
import utils
from typing import (
    Mapping,
    Sequence,
    Any,
)

class TestAccessNestedMap(unittest.TestCase):
    """Tests for utils.access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Tests utils.access_nested_map with various inputs."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)
      @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
     
             def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
        """Tests utils.access_nested_map for expected KeyError exceptions."""
              with self.assertRaises(KeyError) as context:
               utils.access_nested_map(nested_map, path)
                 self.assertEqual(str(context.exception), str(path[-1]))

if __name__ == '__main__':
    unittest.main()
