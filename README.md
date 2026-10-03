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

## 📖 Getting Started

Let's walk through a simple example to see how tkweb works:

1. **Install tkweb**:
   ```bash
   pip install tkweb
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

### Using pip (Recommended)
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
Python, `pipx install tkweb` is another safe option. On Debian/Ubuntu, install
the virtual-environment support first if it is missing:

```bash
sudo apt install python3-venv python3-full
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
# Option 1: Recommended - Create a virtual environment
python3 -m venv tkweb-env
source tkweb-env/bin/activate
pip install tkweb

# Option 2: Using pipx (if installed)
# pipx install tkweb

# Option 3: System-wide installation (NOT RECOMMENDED for production)
# pip install --break-system-packages tkweb  # Use at your own risk!

# Install system dependencies if needed
sudo apt update && sudo apt install -y python3-venv python3-pip
```

#### 🍎 macOS
```bash
# Using Homebrew (if you have it)
brew install python  # Ensures you have pip3
pip3 install tkweb

# Or using the official Python installer
# Download from https://python.org, then:
pip3 install tkweb

# Or create a virtual environment (recommended)
python3 -m venv tkweb-env
source tkweb-env/bin/activate
pip install tkweb
```

#### 💻 Windows
```powershell
# Using PowerShell
python -m pip install --upgrade pip
pip install tkweb

# Or using the Microsoft Store Python app
# Install Python from Microsoft Store, then:
python -m pip install tkweb

# Or create a virtual environment (recommended)
python -m venv tkweb-env
tkweb-env\Scripts\activate
pip install tkweb
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

Follow these steps to resolve it without installing additional packages beyond what's already provided by the system:

1. **Remove any existing virtual environment** (optional but recommended):
   ```bash
   rm -rf .venv
   ```

2. **Create a virtual environment that includes system site packages**:
   ```bash
   python3 -m venv .venv --system-site-packages
   ```

3. **Verify the required packages are accessible** (they are already installed via `apt`):
   ```bash
   .venv/bin/python -c "import requests; import bs4; import lxml; import html2text; import tiktoken; print('All packages available')"
   ```
   Output: `All packages available`

4. **Run your code using the virtual environment's Python**:
   - For general scripts:
     ```bash
     .venv/bin/python your_script.py
     ```
   - If your code lives in `src/` and you need to import your local module (e.g., `tkweb`), set `PYTHONPATH`:
     ```bash
     PYTHONPATH=src .venv/bin/python your_script.py
     ```

   Or, to run the example script (note: the example requires internet access which may not be available in this sandbox):
   ```bash
   PYTHONPATH=src .venv/bin/python example.py
   ```

**Why this works**: The system already provides the exact packages listed in your `requirements.txt` via Debian's `apt`:
- `python3-requests` (version 2.32.3) → satisfies `requests>=2.25.1`
- `python3-bs4` (version 4.13.4) → satisfies `beautifulsoup4>=4.9.0`
- `python3-lxml` (version 5.4.0) → satisfies `lxml>=4.6.0`
- `python3-html2text` (version 2025.4.15) → satisfies `html2text>=2020.1.16`
- `python3-tiktoken` (version 0.9.0) → satisfies `tktoken>=0.4.0`

By creating a virtual environment with `--system-site-packages`, you gain access to these system-installed packages without needing to install anything via `pip`, thus avoiding the externally-managed-environment error.

> **Note**: If you need to install additional packages not available via `apt`, you would need network access (or a local package mirror), which may not be available in this environment.
