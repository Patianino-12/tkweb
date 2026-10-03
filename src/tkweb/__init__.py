"""Token-aware Web Scraper (tkweb) - A package for efficient web content processing."""

from .scraper import TokenAwareScraper
from .processor import ContentProcessor
from .utils import calculate_token_savings, format_content_for_ai

__version__ = "0.1.1"
__author__ = "Damiano Iannone"
__email__ = "damiano@example.com"

__all__ = [
    "TokenAwareScraper",
    "ContentProcessor",
    "calculate_token_savings",
    "format_content_for_ai"
]
