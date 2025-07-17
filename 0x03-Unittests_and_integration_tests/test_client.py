#!/usr/bin/env python3
"""Test suite for client.py"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Tests that GithubOrgClient.org returns the correct value."""
        client = GithubOrgClient(org_name)
        client.org()
        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Tests that GithubOrgClient._public_repos_url returns the expected
        URL based on the mocked payload.
        """
        mocked_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock, return_value=mocked_payload):
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url, mocked_payload["repos_url"])


if __name__ == '__main__':
    unittest.main()
