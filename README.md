# 🚀 tkweb - Token-aware Web Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/Patianino-12/tkweb/actions)
[![PyPI](https://img.shields.io/pypi/v/tkweb.svg)](https://pypi.org/project/tkweb/)

> **Scrape smarter, not harder** - Reduce web content from thousands to hundreds of tokens while preserving essential information for AI models.

## ✨ Why tkweb?

When preparing web content for AI models, token efficiency matters. tkweb intelligently scrapes and processes web pages to minimize token usage while maximizing information retention - inspired by the RTK (Rust Token Killer) concept.

### 🚀 One-Line Installation
```bash
pip install tkweb
```

## 📖 Usage Examples

### As a Library
```python
from tkweb import TokenAwareScraper

# Initialize with your target AI model
scraper = TokenAwareScraper(model_name="gpt-4")

# Scrape and optimize in one go
result = scraper.scrape_url(
    'https://example.com/news/article', 
    max_tokens=800,
    remove_selectors=['nav', 'footer', '.sidebar', '.ads']
)

print(f"✅ Scraped {result['token_count']} tokens (saved {result['token_savings']:.1%})")
print(result['content'][:200] + "...")

# Or process existing text
from tkweb.processor import process_for_ai_consumption
optimized = process_for_ai_consumption(raw_text, max_tokens=500)
```

### Command Line Interface
```bash
# Basic scraping with token limit
tkweb scrape https://example.com --max-tokens 500

# Save to file with custom output
tkweb scrape https://example.com --output article.json --format json

# Process existing content
cat article.txt | tkweb process --max-tokens 300 --aggressive

# Run the demonstration
tkweb demo
```

## 🔧 How It Works

tkweb employs a 6-stage optimization pipeline:

1. **🌐 HTML Cleaning** - Removes nav, footer, ads, scripts
2. **🧹 Text Normalization** - Fixes whitespace and formatting
3. **🗑️ Boilerplate Detection** - Eliminates cookie notices, copyrights, etc.
4. **🎯 Content Extraction** - Heuristic-based main content identification
5. **🔢 Token Counting** - Accurate counting via tiktoken for specific models
6. **✂️ Intelligent Truncation** - Preserves key information while fitting limits

## ⚙️ Configuration

Customize behavior to match your needs:
```python
scraper = TokenAwareScraper(
    model_name="gpt-4",           # Target AI model for counting
    remove_selectors=[            # Elements to remove
        'nav', 'footer', '.sidebar', 
        '.ads', '.comments', '.related'
    ]
)

# Process with aggressive optimization for extreme cases
result = scraper.scrape_url(url, max_tokens=300, aggressive=True)
```

## 📦 Installation

### Using pip (Recommended)
```bash
# Install from PyPI
pip install tkweb

# Or install in development mode
git clone https://github.com/Patianino-12/tkweb.git
cd tkweb
pip install -e .
```

### Alternative Installation Methods

#### Using conda (Anaconda/Miniconda)
```bash
conda install -c conda-forge tkweb
```

#### Using pipx (for isolated CLI tools)
```bash
pipx install tkweb
```

#### From source (all platforms)
```bash
# Download and extract
curl -L https://github.com/Patianino-12/tkweb/archive/refs/heads/main.zip -o tkweb.zip
unzip tkweb.zip
cd tkweb-main
pip install .
```

### OS-Specific Instructions

#### 🐧 Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt update && sudo apt install -y python3-pip python3-venv

# Install tkweb
pip3 install tkweb
```

#### 🍎 macOS
```bash
# Using Homebrew (if you have it)
brew install python  # Ensures you have pip3
pip3 install tkweb

# Or using the official Python installer
# Download from https://python.org, then:
pip3 install tkweb
```

#### 💻 Windows
```powershell
# Using PowerShell
python -m pip install --upgrade pip
pip install tkweb

# Or using the Microsoft Store Python app
# Install Python from Microsoft Store, then:
python -m pip install tkweb
```

### Verifying Installation
```bash
tkweb --version
# Should show: tkweb 0.1.0 or higher
```

## 📋 Requirements

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- html2text
- tiktoken

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE] file for details.

## 🙏 Inspiration

This project draws inspiration from the [RTK (Rust Token Killer)](https://github.com/Kosciuszko/rtk) concept, which focuses on reducing token usage when interacting with AI models by filtering and optimizing content before it reaches the model's context window.

---

*Made with ❤️ for efficient AI development. Scrape smarter!*