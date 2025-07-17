#!/usr/bin/env python3
"""Test suite for utils.py"""
import unittest
from unittest.mock import patch, Mock
from utils import get_json


class TestGetJson(unittest.TestCase):
    """Tests the get_json function."""

    @patch('requests.get')
    def test_get_json(self, mock_get):
        """Tests that get_json returns the expected result."""
        test_cases = [
            {"test_url": "http://example.com", "test_payload": {"payload": True}},
            {"test_url": "http://holberton.io", "test_payload": {"payload": False}},
        ]

        for case in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = case["test_payload"]
            mock_get.return_value = mock_response

            result = get_json(case["test_url"])

            mock_get.assert_called_once_with(case["test_url"])
            self.assertEqual(result, case["test_payload"])


if __name__ == '__main__':
    unittest.main()
