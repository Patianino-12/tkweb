"""
Tests for the tkweb scraper module.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path so we can import tkweb
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tkweb.scraper import TokenAwareScraper


class TestTokenAwareScraper(unittest.TestCase):
    """Test cases for TokenAwareScraper."""

    def setUp(self):
        """Set up test fixtures."""
        self.scraper = TokenAwareScraper()

    def test_initialization(self):
        """Test that the scraper initializes correctly."""
        self.assertIsNotNone(self.scraper.encoding)
        self.assertEqual(self.scraper.model_name, "gpt-3.5-turbo")

    def test_count_tokens(self):
        """Test token counting functionality."""
        text = "Hello world"
        tokens = self.scraper.count_tokens(text)
        self.assertIsInstance(tokens, int)
        self.assertGreater(tokens, 0)

    @patch('tkweb.scraper.requests.get')
    def test_scrape_url_success(self, mock_get):
        """Test successful URL scraping."""
        # Mock response
        mock_response = Mock()
        mock_response.content = b'<html><body><h1>Test</h1><p>This is a test.</p></body></html>'
        mock_response.text = '<html><body><h1>Test</h1><p>This is a test.</p></body></html>'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.scraper.scrape_url('http://example.com')

        self.assertIn('url', result)
        self.assertIn('content', result)
        self.assertIn('token_count', result)
        self.assertEqual(result['url'], 'http://example.com')
        self.assertIsInstance(result['token_count'], int)
        self.assertGreaterEqual(result['token_count'], 0)

    @patch('tkweb.scraper.requests.get')
    def test_scrape_url_with_max_tokens(self, mock_get):
        """Test scraping with token limit."""
        # Mock response with lots of content
        large_content = '<html><body>' + '<p>This is a test paragraph. </p>' * 100 + '</body></html>'
        mock_response = Mock()
        mock_response.content = large_content.encode('utf-8')
        mock_response.text = large_content
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.scraper.scrape_url('http://example.com', max_tokens=50)

        self.assertLessEqual(result['token_count'], 50)
        self.assertIn('content', result)

    @patch('tkweb.scraper.requests.get')
    def test_scrape_url_error(self, mock_get):
        """Test handling of HTTP errors."""
        mock_get.side_effect = Exception("Network error")

        with self.assertRaises(Exception):
            self.scraper.scrape_url('http://example.com')


if __name__ == '__main__':
    unittest.main()