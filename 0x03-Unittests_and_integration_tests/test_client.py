#!/usr/bin/env python3
"""Test suite for client.py"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
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
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock,
                   return_value=mocked_payload) as mock_org_property:
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url,
                             mocked_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Tests that GithubOrgClient.public_repos returns the expected
        list of repos.
        """
        mocked_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mocked_repos_payload
        mocked_repos_url = "https://api.github.com/orgs/test_org/repos"

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value=mocked_repos_url) as mock_public_repos_url:
            client = GithubOrgClient("test_org")
            repos = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mocked_repos_url)


if __name__ == '__main__':
    unittest.main()
