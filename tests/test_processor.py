"""
Tests for the tkweb processor module.
"""

import unittest
import sys
import os

# Add src to path so we can import tkweb
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tkweb.processor import ContentProcessor, process_for_ai_consumption
from tkweb.utils import calculate_token_savings


class TestContentProcessor(unittest.TestCase):
    """Test cases for ContentProcessor."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = ContentProcessor()
        self.sample_text = """
        This is a test article.

        It has multiple paragraphs and some extra whitespace.

        The quick brown fox jumps over the lazy dog.

        Copyright 2023 Example Corp. All rights reserved.
        """

    def test_remove_extra_whitespace(self):
        """Test whitespace removal."""
        text = "  This   is   a   test  \n\n\n  with  extra   whitespace  "
        result = self.processor.remove_extra_whitespace(text)
        self.assertEqual(result, "This is a test\n\nwith extra whitespace")

    def test_remove_boilerplate(self):
        """Test boilerplate removal."""
        text = "This is real content.\n\nCookie policy: We use cookies.\n\nMore real content."
        result = self.processor.remove_boilerplate(text)
        self.assertNotIn("Cookie policy", result)
        self.assertIn("This is real content", result)
        self.assertIn("More real content", result)

    def test_extract_key_sentences(self):
        """Test key sentence extraction."""
        text = "Short. This is a medium length sentence with good content. Another short one."
        result = self.processor.extract_key_sentences(text, max_sentences=1)
        # Should return the medium length sentence
        self.assertIn("medium length sentence", result)

    def test_summarize_aggressively(self):
        """Test aggressive summarization."""
        text = "A. B. C. D. E."  # 5 sentences
        result = self.processor.summarize_aggressively(text, ratio=0.4)
        # Should keep about 2 sentences
        self.assertLessEqual(len(result.split('.')), 3)  # Account for empty split

    def test_extract_main_content_hints(self):
        """Test main content extraction."""
        text = "\n\nMenu\nHome\nAbout\nContact\n\nThis is the main article content. It should be preserved.\n\nFooter\nCopyright 2023\n"
        result = self.processor.extract_main_content_hints(text)
        self.assertIn("main article content", result)
        # Should reduce menu/footer content


class TestProcessForAiConsumption(unittest.TestCase):
    """Test cases for process_for_ai_consumption function."""

    def test_basic_processing(self):
        """Test basic text processing."""
        text = "This is a test.  \n\n  With extra whitespace.  \n\nCopyright 2023."
        result = process_for_ai_consumption(text)

        self.assertIn('processed_text', result)
        self.assertIn('original_token_estimate', result)
        self.assertIn('processed_token_estimate', result)
        self.assertIn('token_savings_ratio', result)

        # Should have reduced length due to whitespace and boilerplate removal
        self.assertLess(len(result['processed_text']), len(text))

    def test_processing_with_max_tokens(self):
        """Test processing with token limit."""
        # Create long text
        text = "This is a test sentence. " * 100
        result = process_for_ai_consumption(text, max_tokens=50)

        # Should respect the token limit (approximately)
        self.assertLessEqual(result['processed_token_estimate'], 60)  # Allow some overhead

    def test_aggressive_processing(self):
        """Test aggressive processing."""
        text = "A. B. C. D. E. F. G."  # Many short sentences
        result = process_for_ai_consumption(text, aggressive=True)

        # Should be significantly shorter
        self.assertLess(len(result['processed_text']), len(text) * 0.5)


class TestCalculateTokenSavings(unittest.TestCase):
    """Test cases for calculate_token_savings function."""

    def test_token_savings_calculation(self):
        """Test token savings calculation."""
        original = "This is a test sentence. " * 10
        processed = "This is a test sentence. " * 5  # Half the content

        savings = calculate_token_savings(original, processed)

        self.assertIn('original_tokens', savings)
        self.assertIn('processed_tokens', savings)
        self.assertIn('tokens_saved', savings)
        self.assertIn('savings_percentage', savings)

        self.assertEqual(savings['tokens_saved'], savings['original_tokens'] - savings['processed_tokens'])
        self.assertGreater(savings['savings_percentage'], 0)

    def test_no_savings_when_same(self):
        """Test zero savings when texts are identical."""
        text = "This is a test."
        savings = calculate_token_savings(text, text)

        self.assertEqual(savings['tokens_saved'], 0)
        self.assertEqual(savings['savings_percentage'], 0)


if __name__ == '__main__':
    unittest.main()