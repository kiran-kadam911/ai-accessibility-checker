import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv
from tabulate import tabulate

# Load API Key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ OpenAI API key not found in .env file.")
    print("Please create a .env file with: OPENAI_API_KEY=your_key_here")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

# Supported file extensions for scanning
SUPPORTED_EXTENSIONS = ['.html', '.twig', '.css', '.scss', '.pcss', '.jsx', '.tsx']

# Excluded directories
EXCLUDED_DIRS = ['node_modules', '.git', '__pycache__', 'dist', 'build']

def get_user_inputs():
    print("👋 Welcome to AI Accessibility Checker\n")
    
    level = input("🧩 Which WCAG accessibility level do you want to check? (A / AA / AAA): ").upper().strip()
    while level not in ["A", "AA", "AAA"]:
        level = input("❗ Please enter a valid level (A / AA / AAA): ").upper().strip()

    version = input("📘 Which WCAG version do you want to check? (2.0 / 2.1 / 2.2): ").strip()
    while version not in ["2.0", "2.1", "2.2"]:
        version = input("❗ Please enter a valid version (2.0 / 2.1 / 2.2): ").strip()

    output_format = input("📊 How would you like results? (table / list): ").strip().lower()
    if output_format not in ["table", "list"]:
        print("⚠️ Invalid choice. Defaulting to 'table'.")
        output_format = "table"

    path = input("📂 Enter the directory path to scan the files (leave blank for current directory): ").strip()
    if not path:
        path = os.getcwd()

    return level, version, output_format, path

def find_supported_files(directory):
    files_to_scan = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDED_DIRS]
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                files_to_scan.append(os.path.join(root, file))
    return files_to_scan

def scan_with_ai(content, file_name, level, version):
    prompt = f"""
You are an expert in web accessibility and WCAG compliance.

The following code includes line numbers.

Scan the code and return **only valid JSON** with this structure:
[
  {{
    "title": "Short title of the issue",
    "issue_type": "Type/category of the issue (e.g., Contrast, Alt Text, Keyboard Navigation)",
    "description": "Detailed description of the issue",
    "line_numbers": [list of affected lines],
    "code_snippet": "Relevant code snippet",
    "suggestion": "AI-based suggestion to fix it",
    "severity": "High | Medium | Low"
  }}
]

Rules:
- Do not include any extra text outside JSON.
- Severity should be based on WCAG impact.
- If no issues found, return [].

WCAG Version: {version}
Accessibility Level: {level}

File: {file_name}
----------------------
{content}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert accessibility auditor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content.strip()
        raw_output = re.sub(r"^```(json)?|```$", "", raw_output, flags=re.MULTILINE).strip()

        match = re.search(r"\[.*\]", raw_output, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            return []

    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parsing error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error scanning file {file_name}: {str(e)}")
        return []

def main():
    level, version, output_format, directory = get_user_inputs()
    files_to_scan = find_supported_files(directory)

    if not files_to_scan:
        print("⚠️ No supported files found in the specified directory.")
        return

    print(f"\n🔍 Scanning {len(files_to_scan)} file(s) for WCAG {version} ({level}) issues...\n")

    for file in files_to_scan:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"📄 Scanning: {file}")
            numbered_content = "\n".join(f"{i+1:4}: {line}" for i, line in enumerate(content.splitlines()))
            issues = scan_with_ai(numbered_content, os.path.basename(file), level, version)

            if not issues:
                print("✅ No accessibility issues found.\n")
                continue

            if output_format == "table":
                table_data = [
                    [
                        i+1,
                        issue.get("title", ""),
                        issue.get("issue_type", ""),
                        issue.get("severity", ""),
                        ", ".join(map(str, issue.get("line_numbers", []))),
                        issue.get("description", ""),
                        issue.get("suggestion", "")
                    ]
                    for i, issue in enumerate(issues)
                ]
                headers = ["#", "Issue Title", "Issue Type", "Severity", "Line(s)", "Description", "Suggestion"]
                print(tabulate(table_data, headers=headers, tablefmt="grid", maxcolwidths=[None, 25, 10, 10, 10, 40, 40]))
                print("\n" + "-"*100 + "\n")

            elif output_format == "list":
                for idx, issue in enumerate(issues, start=1):
                    print(f"\n{idx}. {issue.get('title', '')} [{issue.get('issue_type', '')}] (Severity: {issue.get('severity', '')})")
                    print(f"   Lines: {', '.join(map(str, issue.get('line_numbers', [])))}")
                    print(f"   Description: {issue.get('description', '')}")
                    print(f"   Suggestion: {issue.get('suggestion', '')}")
                    print("-"*80)

        except Exception as e:
            print(f"❗ Could not read {file}: {str(e)}")

if __name__ == "__main__":
    main()
