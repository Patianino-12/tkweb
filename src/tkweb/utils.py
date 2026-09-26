"""
Utility functions for token-aware web scraping.
"""

import tiktoken
from typing import Optional


def calculate_token_savings(original_text: str, processed_text: str,
                          model_name: str = "gpt-3.5-turbo") -> dict:
    """
    Calculate token savings between original and processed text.

    Args:
        original_text: The original text content
        processed_text: The processed/optimized text content
        model_name: The model to use for token counting

    Returns:
        Dictionary with token counts and savings percentage
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    original_tokens = len(encoding.encode(original_text))
    processed_tokens = len(encoding.encode(processed_text))

    if original_tokens == 0:
        savings_percentage = 0
    else:
        savings_percentage = ((original_tokens - processed_tokens) / original_tokens) * 100

    return {
        'original_tokens': original_tokens,
        'processed_tokens': processed_tokens,
        'tokens_saved': original_tokens - processed_tokens,
        'savings_percentage': max(0, savings_percentage)
    }


def format_content_for_ai(content: str, max_tokens: int = 2000,
                         model_name: str = "gpt-3.5-turbo") -> str:
    """
    Format content to fit within token limits for AI consumption.

    Args:
        content: The content to format
        max_tokens: Maximum tokens allowed
        model_name: The model to use for token counting

    Returns:
        Content truncated to fit within token limits
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(content)
    if len(tokens) <= max_tokens:
        return content

    # Truncate to max_tokens
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)


def estimate_reading_time(text: str, wpm: int = 200) -> float:
    """
    Estimate reading time for text in minutes.

    Args:
        text: The text to estimate reading time for
        wpm: Words per minute for reading speed

    Returns:
        Estimated reading time in minutes
    """
    words = len(text.split())
    return words / wpm if wpm > 0 else 0


def extract_metadata_from_html(html_content: str) -> dict:
    """
    Extract basic metadata from HTML content.

    Args:
        html_content: Raw HTML content

    Returns:
        Dictionary with metadata like title, description, etc.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {}

    # Extract title
    title_tag = soup.find('title')
    metadata['title'] = title_tag.get_text().strip() if title_tag else ''

    # Extract meta description
    description_tag = soup.find('meta', attrs={'name': 'description'})
    if not description_tag:
        description_tag = soup.find('meta', attrs={'property': 'og:description'})
    metadata['description'] = description_tag.get('content', '').strip() if description_tag else ''

    # Extract author
    author_tag = soup.find('meta', attrs={'name': 'author'})
    if not author_tag:
        author_tag = soup.find('meta', attrs={'property': 'article:author'})
    metadata['author'] = author_tag.get('content', '').strip() if author_tag else ''

    # Extract publish date
    date_tag = soup.find('meta', attrs={'property': 'article:published_time'})
    if not date_tag:
        date_tag = soup.find('meta', attrs={'name': 'publish_date'})
    metadata['publish_date'] = date_tag.get('content', '').strip() if date_tag else ''

    return metadata