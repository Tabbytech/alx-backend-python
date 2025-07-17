#!/usr/bin/env python3
"""Test suite for client.py"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


TESTS_PAYLOAD = TEST_PAYLOAD[0][1]
ORG_PAYLOAD = TEST_PAYLOAD[0][0]


@parameterized_class([
    {
        'org_payload': ORG_PAYLOAD,
        'repos_payload': TESTS_PAYLOAD,
        'expected_repos': [
            'episodes.dart', 'cpp-netlib', 'dagger', 'ios-webkit-debug-proxy',
            'google.github.io'
        ],
        'apache2_repos': []
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect for mocking requests.get."""
            if url == GithubOrgClient.ORG_URL.format(org=cls.ORG_PAYLOAD['login']):
                return Mock(json=lambda: cls.org_payload)
            if url == cls.org_payload['repos_url']:
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: [])

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class for integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Tests that GithubOrgClient.public_repos returns the correct list
        of repos in an integration scenario.
        """
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Tests that GithubOrgClient.public_repos with a license filter returns
        the correct list of repos in an integration scenario.
        """
        client = GithubOrgClient(self.org_payload['login'])
        apache2_repos = [repo["name"] for repo in self.repos_payload
                         if repo["license"]["key"] == "apache-2.0"]
        self.assertEqual(client.public_repos(license="apache-2.0"), apache2_repos)


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Tests that GithubOrgClient.has_license returns the expected
        boolean.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
