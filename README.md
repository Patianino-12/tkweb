# 🚀 tkweb - Token-aware Web Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/Patianino-12/tkweb/actions)
[![PyPI](https://img.shields.io/pypi/v/tkweb.svg)](https://pypi.org/project/tkweb/)

> **Scrape smarter, not harder** - Reduce web content from thousands to hundreds of tokens while preserving essential information for AI models.

## ✨ Why tkweb?

When preparing web content for AI models, token efficiency matters. tkweb intelligently scrapes and processes web pages to minimize token usage while maximizing information retention - inspired by the RTK (Rust Token Killer) concept.

### 🚀 Installation

This is the safe installation process for Debian, Ubuntu, and other systems
that implement PEP 668:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install tkweb
```

## 📖 Getting Started

The CLI examples below assume that the virtual environment containing `tkweb`
is active. If you have not activated it, run:

```bash
source .venv/bin/activate
```

You can also invoke the executable directly without activating the environment:

```bash
.venv/bin/tkweb --help
```

Let's walk through a simple example to see how tkweb works:

1. **Install tkweb**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install tkweb
   ```

2. **Scrape a webpage with token limits**:
   ```bash
   # This will scrape the URL and limit the output to ~500 tokens
   tkweb scrape https://httpbin.org/html --max-tokens 500
   ```

3. **Save the results to a file**:
   ```bash
   tkweb scrape https://httpbin.org/html --max-tokens 300 --output scraped_content.txt
   ```

4. **Process existing text content**:
   ```bash
   echo "Your long text goes here..." | tkweb process --max-tokens 100
   ```

## 📚 Detailed Usage Examples

### As a Library
```python
from tkweb import TokenAwareScraper

# Initialize the scraper with your target AI model
# This ensures accurate token counting for models like GPT-4, Claude, etc.
scraper = TokenAwareScraper(model_name="gpt-4")

# Scrape and optimize a webpage in one step
# Parameters:
#   url: The webpage to scrape
#   max_tokens: Maximum number of tokens to return (None for no limit)
#   remove_selectors: CSS selectors of elements to remove (ads, nav, etc.)
result = scraper.scrape_url(
    'https://example.com/news/article', 
    max_tokens=800,
    remove_selectors=['nav', 'footer', '.sidebar', '.ads']
)

# The result is a dictionary containing:
print(f"✅ Successfully scraped and processed!")
print(f"📊 Original tokens: {result['original_token_count']}")
print(f"📉 Processed tokens: {result['token_count']}")
print(f"💰 Token savings: {result['token_savings']:.1%}")
print(f"📄 Content preview: {result['content'][:150]}...")

# Access the full processed content
full_content = result['content']

# Get metadata about the scraping process
metadata = result['metadata']
print(f"🔗 Final URL: {metadata.get('final_url')}")
print(f"📈 Status code: {metadata.get('status_code')}")

# Or process existing text content directly
from tkweb.processor import process_for_ai_consumption

# If you already have text content (from a file, API, etc.)
raw_text = "Your very long text content that needs to be optimized for AI consumption..."
optimized_result = process_for_ai_consumption(
    raw_text, 
    max_tokens=500,           # Target token limit
    aggressive=False          # Set to True for maximum compression
)

print(f"🔧 Optimization complete: {len(raw_text)} → {len(optimized_result['content'])} characters")
```

### Command Line Interface

Activate the environment first, or replace `tkweb` with `.venv/bin/tkweb`:

```bash
source .venv/bin/activate
```

```bash
# 🔍 Basic scraping with default settings
# Uses reasonable defaults for element removal and no token limit
tkweb scrape https://example.com

# 🎯 Scrape with specific token limit
# Returns content limited to approximately 500 tokens
tkweb scrape https://example.com --max-tokens 500

# 💾 Save scraping results to a file
# --output specifies the file path, --format chooses output format
tkweb scrape https://example.com \
    --max-tokens 300 \
    --output article.txt \
    --format text

# 📊 Get detailed results in JSON format
# Includes token counts, savings percentage, and metadata
tkweb scrape https://example.com \
    --max-tokens 400 \
    --output result.json \
    --format json

# ⚙️ Process existing text content from a file or pipe
# Read from file and optimize for AI consumption
cat long_article.txt | tkweb process --max-tokens 250

# 🚀 Use aggressive mode for maximum compression
# Ideal when you need to fit content into very tight token limits
cat documentation.pdf | tkweb process --max-tokens 150 --aggressive

# 🎪 Run the built-in demonstration
# Shows tkweb in action with example websites
tkweb demo

# ❓ Get help and see all available options
tkweb --help
tkweb scrape --help
tkweb process --help
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
    model_name="gpt-4",           # Target AI model for counting (gpt-4, gpt-3.5-turbo, claude-2, etc.)
    remove_selectors=[            # Elements to remove during scraping
        'nav', 'footer', '.sidebar', 
        '.ads', '.comments', '.related', '.menu'
    ]
)

# Process with aggressive optimization for extreme cases
# aggressive=True uses more aggressive summarization techniques
result = scraper.scrape_url(url, max_tokens=300, aggressive=True)
```

## 📦 Installation

### Using a virtual environment (Recommended)
```bash
# Debian, Ubuntu, and other PEP 668-compliant systems require a virtual environment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install tkweb

# Or install in development mode
git clone https://github.com/Patianino-12/tkweb.git
cd tkweb
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

If you only need the `tkweb` command and do not need to import the package from
Python, `pipx` is another safe option:

```bash
sudo apt install pipx
pipx install tkweb
pipx ensurepath
```

### Alternative Installation Methods

#### Using conda (Anaconda/Miniconda)
```bash
conda install -c conda-forge tkweb
```

#### Using pipx (for isolated CLI tools)
```bash
sudo apt install pipx
pipx install tkweb
pipx ensurepath
```

#### From source (all platforms)
```bash
# Download and extract
curl -L https://github.com/Patianino-12/tkweb/archive/refs/heads/main.zip -o tkweb.zip
unzip tkweb.zip
cd tkweb-main
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

### OS-Specific Instructions

#### 🐧 Linux (Ubuntu/Debian)
```bash
# Option 1: Recommended - Create a virtual environment
python3 -m venv tkweb-env
source tkweb-env/bin/activate
python -m pip install tkweb

# Option 2: Using pipx (if installed)
pipx install tkweb

# Install the virtual-environment support if needed
sudo apt update && sudo apt install -y python3-venv python3-pip
```

#### 🍎 macOS
```bash
# Create a virtual environment (recommended)
python3 -m venv tkweb-env
source tkweb-env/bin/activate
python -m pip install tkweb
```

#### 💻 Windows
```powershell
# Create a virtual environment (recommended)
python -m venv tkweb-env
tkweb-env\Scripts\activate
python -m pip install tkweb
```

### Verifying Installation
```bash
source .venv/bin/activate
tkweb --version
# Should show: tkweb 0.1.1
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

## 🛠️ Fixing the 'externally-managed-environment' error

If you encounter the error:
```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.13/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

Follow these steps to resolve it:

1. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   ```

2. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

3. **Install and verify tkweb**:
   ```bash
   python -m pip install tkweb
   tkweb --version
   ```

If your system does not include the `venv` module:

```bash
sudo apt install python3-venv python3-full
```

Do not use `pip install --break-system-packages` unless you intentionally accept
the risk of replacing packages managed by the operating system.
