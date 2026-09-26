# tkweb - Token-aware Web Scraper

## Overview

I've created a Python package called **tkweb** (Token-aware Web Scraper) that implements token-efficient web content extraction for AI consumption. This project demonstrates the principles of token optimization similar to the RTK (Rust Token Killer) concept mentioned in the instructions.

## Features Implemented

### Core Functionality
1. **Token-aware Web Scraping** - Scrapes web content while being conscious of token usage for AI models
2. **Content Processing Pipeline** - Multiple stages of content optimization:
   - Boilerplate removal (cookie notices, copyright, nav bars, etc.)
   - Whitespace normalization
   - Main content extraction using heuristics
   - Key sentence extraction for token budgeting
   - Aggressive summarization for extreme cases
3. **Token Counting** - Accurate token counting using tiktoken for specific AI models
4. **Flexible CLI** - Command-line interface with multiple commands and options

### Technical Implementation
- **Modular Design** - Separate modules for scraping, processing, utilities, and CLI
- **Proper Error Handling** - Graceful handling of network errors, parsing issues, etc.
- **Type Hints** - Full type annotations for better code maintainability
- **Comprehensive Testing** - Unit tests for all major components
- **Documentation** - README with usage examples, API documentation, and project overview
- **Installation Setup** - setuptools-based installation with console script entry point

### Key Components

1. **TokenAwareScraper Class** (`src/tkweb/scraper.py`)
   - Fetches and parses web content
   - Removes unwanted elements (nav, footer, ads, etc.)
   - Extracts clean text content
   - Counts tokens using tiktoken
   - Truncates content to specified token limits

2. **ContentProcessor Class** (`src/tkweb/processor.py`)
   - Boilerplate removal using regex patterns
   - Whitespace normalization
   - Main content extraction heuristics
   - Key sentence extraction based on scoring algorithms
   - Aggressive summarization for extreme token reduction

3. **Utility Functions** (`src/tkweb/utils.py`)
   - Token savings calculation
   - Content formatting for AI consumption limits
   - HTML metadata extraction
   - Reading time estimation

4. **Command-line Interface** (`src/tkweb/cli.py`)
   - `scrape` command: Scrape URLs with token limits
   - `process` command: Process text content from stdin/files
   - `demo` command: Run demonstration with example URLs
   - Multiple output formats (text, JSON, metadata)
   - Verbose logging option

5. **Testing Suite** (`tests/`)
   - Unit tests for scraper functionality
   - Unit tests for processor functionality
   - Tests for edge cases and error conditions

## Usage Examples

### As a Library
```python
from tkweb import TokenAwareScraper

scraper = TokenAwareScraper()
result = scraper.scrape_url('https://example.com/article', max_tokens=1000)
print(f"Extracted {result['token_count']} tokens")
print(result['content'])
```

### Command Line
```bash
# Basic scraping
tkweb scrape https://example.com

# Scrape with token limit
tkweb scrape https://example.com --max-tokens 500

# Process existing content
cat article.txt | tkweb process --max-tokens 300

# Run demonstration
tkweb demo
```

## Design Principles

Following the RTK (Rust Token Killer) inspiration:
- **Pre-processing Optimization** - Reduce token usage before content reaches AI models
- **Intelligent Content Selection** - Preserve information density while minimizing tokens
- **Configurable Reduction** - Adjustable token limits and processing aggressiveness
- **Model-aware Token Counting** - Accurate counting for specific AI architectures
- **Progressive Reduction Strategy** - Multiple levels of optimization based on needs

## Files Created

```
src/tkweb/                 # Main package source
├── __init__.py           # Package exports
├── scraper.py            # Web scraping logic
├── processor.py          # Content processing
├── utils.py              # Helper functions
└── cli.py                # Command-line interface

tests/                    # Test suite
├── test_scraper.py       # Scraper tests
└── test_processor.py     # Processor tests

example.py                # Usage examples
README.md                 # Project documentation
PROJECT_SUMMARY.md        # This summary
requirements.txt          # Dependencies
setup.py                  # Installation configuration
pyproject.toml            # Build configuration
```

## Testing Results

All 15 unit tests pass:
- 5 scraper tests ✓
- 10 processor tests ✓

## Future Enhancements

Potential improvements for future development:
- Integration with actual RTK library for enhanced token optimization
- More sophisticated NLP-based content extraction
- Support for additional output formats (JSON-LD, XML, etc.)
- Caching mechanism for repeated URL requests
- Batch processing capabilities
- Web interface or API service wrapper
- Integration with popular AI frameworks (LangChain, LlamaIndex, etc.)

## Conclusion

This tkweb project successfully demonstrates token-aware web scraping principles that align with the RTK concept shown in the instructions. It provides practical tools for reducing token consumption when preparing web content for AI model input, addressing a real-world challenge in efficient AI applications.