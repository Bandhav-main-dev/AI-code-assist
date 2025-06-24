# 🤖 Gemini AI Code Assistant

An AI-powered assistant using **Google Gemini** to:
- ✅ Auto-correct Python errors
- 🧠 Fix code based on manual error input
- 🛠 Generate Python code from plain algorithms
- 📜 Log all changes with summaries and timestamps
- 🔐 Validate your Gemini API setup and list available models

---

## 📁 Project Structure

```
ai_code_assist.py        # Main assistant script
api_check.py             # Script to test Gemini API key & list available models
logs.txt                 # Logs all changes made by AI
*.py                     # Your Python files to correct/test
main.py / app.py / ...   # Entry point(s) (optional)
```

---

## ⚙️ Features

### ✅ Auto Error Correction
- Scans all `.py` files.
- Uses Gemini to fix code errors automatically.

### 🧠 Manual Error Fixing
- Accepts user-provided errors and instructions to guide Gemini fixes.

### 📄 Algorithm to Python Code
- Converts plain English steps into working Python code.

### 📝 Change Logging
- Logs all code updates in `logs.txt`, including:
  - 🕒 Timestamp
  - 📄 File path
  - 🔄 Change reason
  - 🧠 Summary of AI changes

### 🔐 Gemini API Model Checker
- `api_check.py` lists all available Gemini models using your API key.
- Helps validate your Gemini API setup and permissions.

---

## 🚀 How to Use

### 1. Run the Assistant

```bash
python ai_code_assist.py
```

Follow the prompts to:
- 📁 Enter your project folder path
- 📄 Enter algorithm text file path
- 📝 Provide optional error messages
- 💬 Add clarifying instructions
- ✅ Choose actions like:
  - Fix files
  - Generate code
  - Run / test / launch project

---

### 2. Check Your API Key and Available Models

```bash
python api_check.py
```

You will see a list of available Gemini models, with:
- Model name
- Description
- Token limits
- Supported generation methods

---

## 🔐 Requirements

- Python 3.7+
- `google-generativeai`
- `python-dotenv` (optional for `.env` support)

---

## 📦 Installation

```bash
pip install google-generativeai python-dotenv
```

---

## 🔑 Setup API Key

### Option 1: Hardcoded (not recommended)

```python
GEMINI_API_KEY = "your-api-key-here"
```

### Option 2: Secure using `.env` file

Create a file named `.env` in your project directory:

```
GEMINI_API_KEY=your-api-key-here
```

Then load it in Python:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 💡 Example

**Sample Algorithm:**
```
Step 1: Ask for two numbers
Step 2: Add them
Step 3: Print the result
```

Save as `calculator_algo.txt`. Run the assistant, and it will generate the Python code.

---

## 🪪 License

MIT License – Free to use, modify, and share.

---

## ✨ Author

Built by **Bandhav Rajyaguru** – combining AI power with smart development workflows.
