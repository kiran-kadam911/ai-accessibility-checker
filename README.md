# ♿ AI Accessibility Checker
A smart Python CLI tool to scan your project’s frontend code for WCAG compliance issues using OpenAI AI analysis.

## Features
- Supports WCAG Levels: A, AA, AAA
- Supports WCAG Versions: 2.0, 2.1, 2.2
- Skips unnecessary folders (node_modules, .git, __pycache__, etc.)
- AI-powered suggestions for each detected issue
- Output in table or list format
- Works as standalone CLI or pre-commit hook

## Detects accessibility problems like:
- ✅ Missing alt attributes
- 🎨 Low contrast text
- ⌨️ Keyboard navigation issues
- 📜 Improper semantic markup
- 🖼️ ARIA misusage
- 🧠 AI-powered suggestions to fix detected issues

## 🧠 How It Works

- Reads files and adds line numbers
- Sends file contents to OpenAI with WCAG context
- AI detects violations and returns JSON
- Script formats and displays results

## ⚙️ Prerequisites
Before using this tool, make sure you have the following installed:
1. **Python 3.9+**
    
    Mac: 

    Python 3 is usually preinstalled. Check with:

    ```bash
    python3 --version
    ```

    If missing, install via Python.org or Homebrew:

    ```bash
    brew install python
    ```

    Windows:

    Download from Python.org
    When installing, make sure to check the box "Add Python to PATH".
    Verify:

    ```bash
    python3 --version
    ```

    Linux:

    ```bash
    sudo apt update && sudo apt install python3 python3-pip -y
    ```

2. **Pip (Python package manager)**

   ```bash
    pip --version
    ```

    If missing:
    ```bash
    python3 -m ensurepip --upgrade
    ```

3. **Virtual Environment (recommended)**

    This avoids dependency conflicts.

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows
    ```

## 📦 Installation

1️⃣ Clone / Copy this script into your project

```bash
git clone git@github.com:kiran-kadam911/ai-accessibility-checker.git
cd ai-accessibility-checker
```

2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

📄 requirements.txt

```bash
python-dotenv
tabulate
openai>=1.0.0
```

## 🔐 Setup OpenAI API Key
You can get your key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys). (for AI suggestions)

To use AI-powered features, you need to provide your OpenAI API key.
    
    bash -c 'read -p "Enter your OpenAI API Key: " key && echo "OPENAI_API_KEY=$key" > .env'

This will generate a .env file in your project root like:

    OPENAI_API_KEY=sk-xxxxxxx

## 🚀 Usage

### Standalone CLI
Run

```bash
python ai_accessibility_checker.py
```

You will be prompted to:

```bash
👋 Welcome to AI Accessibility Checker

🧩 Which WCAG accessibility level do you want to check? (A / AA / AAA):
📘 Which WCAG version do you want to check? (2.0 / 2.1 / 2.2): 
📊 How would you like results? (table / list): 
📂 Enter the directory path to scan the files (leave blank for current directory): 
```

**Example Output (Table)**
| #  | Issue Title           | Type      | Severity | Line(s)      | Description | Suggestion |
|----|-----------------------|-----------|----------|--------------|-------------|------------|
| 1  | Low contrast for text | Contrast  | High     | 25, 29, 231, 233 | Text has low contrast due to faint opacity, making it hard for visually impaired users. | Increase opacity to ≥0.5 to meet contrast ratio requirements. |

**Example Output (List)**

**Missing Alt Text on Image** [Alt Text] _(Severity: High)_
   - **Lines:** 15  
   - **Description:** `<img>` lacks `alt` attribute for screen readers.  
   - **Suggestion:** Add descriptive `alt` text to all `<img>` elements.

### 📂 Supported File Types

```bash
.html, .twig
.css, .scss, .pcss
.jsx, .tsx
```
