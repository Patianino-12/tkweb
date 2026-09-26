# tkweb - Token-aware Web Scraper

A Python package for scraping web content optimized for token efficiency when feeding to AI models. Inspired by the RTK (Rust Token Killer) concept, tkweb helps reduce token usage by removing boilerplate, extracting key content, and providing token-aware scraping capabilities.

## Features

- **Token-aware scraping**: Count and limit tokens when scraping web content
- **Boilerplate removal**: Automatically remove navigation, footers, ads, and other non-content elements
- **Content extraction**: Heuristic-based extraction of main article/content
- **Token budgeting**: Set maximum token limits per URL or across multiple URLs
- **Multiple output formats**: Text, JSON, or metadata-only output
- **CLI interface**: Easy-to-use command-line tool
- **Library API**: Programmable interface for integration into other applications

## Installation

```bash
pip install -e .
```

Or install from PyPI (when available):

```bash
pip install tkweb
```

## Usage

### As a Library

```python
from tkweb import TokenAwareScraper

# Initialize scraper
scraper = TokenAwareScraper()

# Scrape a URL with token limit
result = scraper.scrape_url('https://example.com/news/article', max_tokens=1000)

print(f"Scraped {result['token_count']} tokens")
print(result['content'])
```

### Command Line Interface

```bash
# Basic scraping
tkweb scrape https://example.com

# Scrape with token limit
tkweb scrape https://example.com --max-tokens 500

# Scrape and save to file
tkweb scrape https://example.com --output article.txt

# Get JSON output with metadata
tkweb scrape https://example.com --format json

# Process existing text content
cat article.txt | tkweb process --max-tokens 300

# Run demonstration
tkweb demo
```

## How It Works

tkweb employs several strategies to minimize token usage:

1. **HTML Cleaning**: Removes common non-content elements (nav, footer, ads, etc.)
2. **Text Normalization**: Cleans up whitespace and formatting
3. **Boilerplate Detection**: Removes common boilerplate text (cookie notices, copyright, etc.)
4. **Content Extraction**: Uses heuristics to identify and prioritize main content
5. **Token Counting**: Uses tiktoken to accurately count tokens for specific AI models
6. **Truncation**: Intelligently truncates content to fit within token limits

## Configuration

You can customize the scraper behavior:

```python
scraper = TokenAwareScraper(model_name="gpt-4")  # Specify model for token counting

# Customize what to remove
result = scraper.scrape_url(
    url,
    remove_selectors=['nav', 'footer', '.sidebar', '.ads', '.comments', '.related']
)
```

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- html2text
- tiktoken

## License

MIT

## Inspiration

This project draws inspiration from the RTK (Rust Token Killer) concept, which focuses on reducing token usage when interacting with AI models by filtering and optimizing content before it reaches the model's context window.