"""
Token-aware web scraper module.

This module provides functionality to scrape web content while being mindful
of token usage for AI consumption, inspired by the RTK (Rust Token Killer) concept.
"""

import requests
from bs4 import BeautifulSoup
import html2text
import tiktoken
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TokenAwareScraper:
    """
    A web scraper that optimizes content for token efficiency when feeding
    to AI models, inspired by RTK principles.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the token-aware scraper.

        Args:
            model_name: The name of the model to use for token counting
        """
        self.model_name = model_name
        try:
            self.encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.encoding = tiktoken.get_encoding("cl100k_base")

        # Configure html2text for clean text extraction
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = True
        self.h2t.ignore_tables = False
        self.h2t.body_width = 0  # Don't wrap text

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens in the text
        """
        return len(self.encoding.encode(text))

    def scrape_url(self, url: str,
                  remove_selectors: Optional[list] = None,
                  max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Scrape a URL and return token-optimized content.

        Args:
            url: The URL to scrape
            remove_selectors: List of CSS selectors to remove (e.g., ['nav', 'footer', '.ads'])
            max_tokens: Maximum tokens to return (will truncate if exceeded)

        Returns:
            Dictionary containing the scraped content and metadata
        """
        if remove_selectors is None:
            remove_selectors = ['nav', 'footer', 'header', '.sidebar', '.ads', '.advertisement']

        try:
            # Fetch the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove unwanted elements
            for selector in remove_selectors:
                for element in soup.select(selector):
                    element.decompose()

            # Extract text content
            text_content = self.h2t.handle(str(soup))

            # Clean up extra whitespace
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            clean_text = '\n'.join(lines)

            # Count tokens
            token_count = self.count_tokens(clean_text)

            # Truncate if max_tokens is specified
            if max_tokens and token_count > max_tokens:
                # Encode and truncate
                encoded = self.encoding.encode(clean_text)
                truncated_encoded = encoded[:max_tokens]
                clean_text = self.encoding.decode(truncated_encoded)
                token_count = max_tokens

            result = {
                'url': url,
                'content': clean_text,
                'token_count': token_count,
                'original_length': len(response.text),
                'cleaned_length': len(clean_text),
                'compression_ratio': len(clean_text) / len(response.text) if len(response.text) > 0 else 0
            }

            logger.info(f"Scraped {url}: {token_count} tokens")
            return result

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            raise

    def scrape_multiple_urls(self, urls: list,
                           max_tokens_per_url: Optional[int] = None,
                           total_max_tokens: Optional[int] = None) -> list:
        """
        Scrape multiple URLs with token limits.

        Args:
            urls: List of URLs to scrape
            max_tokens_per_url: Maximum tokens per URL
            total_max_tokens: Maximum total tokens across all URLs

        Returns:
            List of scraped content dictionaries
        """
        results = []
        total_tokens_used = 0

        for url in urls:
            # Check if we've exceeded total token limit
            if total_max_tokens and total_tokens_used >= total_max_tokens:
                logger.warning(f"Total token limit ({total_max_tokens}) reached. Stopping.")
                break

            # Calculate remaining tokens for this URL
            remaining_tokens = None
            if total_max_tokens:
                remaining_tokens = total_max_tokens - total_tokens_used
                if max_tokens_per_url:
                    remaining_tokens = min(max_tokens_per_url, remaining_tokens)
            elif max_tokens_per_url:
                remaining_tokens = max_tokens_per_url

            try:
                result = self.scrape_url(url, max_tokens=remaining_tokens)
                results.append(result)
                total_tokens_used += result['token_count']

                logger.info(f"Processed {url}: {result['token_count']} tokens "
                           f"(total: {total_tokens_used})")

            except Exception as e:
                logger.error(f"Failed to scrape {url}: {str(e)}")
                # Continue with other URLs even if one fails
                continue

        return results


def quick_scrape(url: str, max_tokens: int = 1000) -> str:
    """
    Convenience function for quick scraping with token limit.

    Args:
        url: URL to scrape
        max_tokens: Maximum tokens to return

    Returns:
        Cleaned text content limited to max_tokens
    """
    scraper = TokenAwareScraper()
    result = scraper.scrape_url(url, max_tokens=max_tokens)
    return result['content']