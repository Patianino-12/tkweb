# Troubleshooting tkweb Installation

## 🚫 `error: externally-managed-environment`

This error comes from Debian, Ubuntu, and other Linux distributions that comply
with [PEP 668](https://peps.python.org/pep-0668/). They deliberately prevent
`pip` from replacing packages managed by the operating system.

Use a virtual environment instead:

```bash
cd /path/to/tkweb
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
tkweb --help
```

If `python3 -m venv` fails, install the required system package first:

```bash
sudo apt install python3-venv python3-full
```

For an isolated command-line installation without manually activating an
environment, use `pipx install tkweb`. Do not use
`pip install --break-system-packages` unless you understand the risk of
breaking the operating system's Python packages.

If you're getting "command not found" when trying to run `tkweb --version`, here are the most common causes and solutions:

## 🔍 Verify Installation

First, check if tkweb is actually installed:

```bash
pip show tkweb
```

If you see output like:
```
Name: tkweb
Version: 0.1.0
Location: /some/path/to/site-packages
...
```
Then the package is installed correctly.

If you get "WARNING: Package(s) not found: tkweb", then it's not installed.

## 🛠️ Common Solutions

### 1. Virtual Environment Not Activated
If you installed tkweb in a virtual environment but forgot to activate it:

```bash
# Activate the virtual environment (adjust path as needed)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Then try again
tkweb --version
```

### 2. User Installation PATH Issue
If you used `pip install --user tkweb`:

```bash
# Find where user-installed packages go
python -m site --user-base

# Add the bin directory to your PATH (add to your shell profile)
export PATH="$PATH:$(python -m site --user-base)/bin"  # Linux/macOS
# or
set "PATH=%PATH%;%APPDATA%\Python\Python39\Scripts"   # Windows (adjust version)
```

### 3. Try Alternative Invocation Methods

Instead of `tkweb`, try:

```bash
# Direct module execution
python -m tkweb --version

# Or if installed in development mode
python -c "from tkweb.cli import main; main()" --version

# Find the exact script location
pip show tkweb | grep Location
# Then look for tkweb script in that directory's bin/ or Scripts/ folder
```

### 4. Reinstall with Explicit PATH

```bash
# Force reinstall and see where it installs
pip install --force-reinstall tkweb --verbose
```

Look for output like:
```
Creating tkweb script in /path/to/bin
```

Make sure that `/path/to/bin` is in your PATH environment variable.

## 📝 For Developers (Installing from Source)

If you cloned the repository and installed from source:

```bash
# Make sure you're in the project directory
cd /path/to/tkweb

# Install in development mode (recommended for developers)
pip install -e .

# This creates a tkweb executable that points to your current code
```

## 🧪 Verify the CLI Module Exists

Check if the CLI module can be imported:

```bash
python -c "import tkweb.cli; print('CLI module found')"
```

If this fails, there may be an installation issue with the package itself.

## 💡 Quick Test

Try running the demonstration directly:

```bash
python -m tkweb demo
```

If this works, then the package is installed correctly and you just need to fix your PATH or activate the right environment.
