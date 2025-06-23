# ai_code_assist.py

import os
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCqiRDczzhwTCoEpi2y1eJlDxuprRZ1qJE"

# ========== 🔧 GEMINI SETUP ==========
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ========== 🤖 GEMINI PROMPTS ==========
def gemini_prompt(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Gemini Error:", e)
        return ""

# ========== 📁 PATH INPUT ==========
def get_project_and_algo_paths():
    while True:
        folder = input("📁 Enter project folder path: ").strip()
        if os.path.isdir(folder):
            break
        print("❌ Invalid folder. Try again.\n")

    while True:
        algo = input("📄 Enter algorithm file path: ").strip()
        if os.path.isfile(algo):
            break
        print("❌ Invalid algorithm file. Try again.\n")

    print(f"✅ Project Folder: {folder}")
    print(f"✅ Algorithm File: {algo}\n")
    return folder, algo

# ========== 🗂 FILE UTILITIES ==========
def read_python_files(folder):
    files = {}
    for root, _, file_list in os.walk(folder):
        for file in file_list:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    files[path] = f.read()
    return files

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def list_all_files(folder):
    return [os.path.join(dp, f) for dp, _, files in os.walk(folder) for f in files]

# ========== 🧠 AI PROCESSING ==========
def correct_errors_with_gemini(code):
    prompt = f"Fix the following Python code. Return corrected and formatted Python code only:\n\n{code}"
    return gemini_prompt(prompt)

def correct_with_manual_error(code, user_error, user_prompt=None):
    prompt = (
        "You are a Python code assistant.\n"
        f"The user reported the following error:\n\n{user_error}\n\n"
        "Fix the following Python code:\n\n"
        f"{code}"
    )
    if user_prompt:
        prompt += f"\n\nUse the following additional instruction to guide your fix:\n{user_prompt}"
    return gemini_prompt(prompt)

def generate_code_from_algorithm(algo_file_path):
    with open(algo_file_path, 'r', encoding='utf-8') as f:
        algo = f.read()
    prompt = f"Convert this algorithm into a working Python program:\n\n{algo}"
    return gemini_prompt(prompt)

# ========== 🚀 MAIN ==========
def main():
    print("🔧 Gemini Code Assistant")
    project_folder, algo_file = get_project_and_algo_paths()

    manual_error = input("\n📝 Optional: Paste any error message you'd like Gemini to fix (or leave blank):\n> ").strip()
    clarify_prompt = ""
    
    clarify_prompt = input("💬 Optional: Add any clarifying instruction to guide Gemini (or leave blank):\n> ").strip()

    print("\n🔍 Reading Python files...")
    python_files = read_python_files(project_folder)

    for path, code in python_files.items():
        print(f"\n📄 Fixing: {path}")
        if manual_error:
            fixed_code = correct_with_manual_error(code, manual_error, clarify_prompt)
        else:
            fixed_code = correct_errors_with_gemini(code)

        if fixed_code.strip():
            write_file(path, fixed_code)
            print(f"✅ Overwritten: {path}")
        else:
            print(f"⚠️ No response from Gemini. File not updated: {path}")

    # Optional: Generate code from algorithm file
    confirm_gen = input("\n🧠 Do you want to generate Python code from the algorithm file? (y/n): ").strip().lower()
    if confirm_gen == 'y':
        new_code = generate_code_from_algorithm(algo_file)
        filename = input("📄 Enter filename to save (e.g., main.py): ").strip()
        save_path = os.path.join(project_folder, filename)
        write_file(save_path, new_code)
        print(f"✅ Generated code saved to: {save_path}")
    else:
        print("🛑 Skipped code generation.")

    print("\n📂 Files in project folder:")
    for file in list_all_files(project_folder):
        print(" -", file)

# ========== 🔧 RUN ==========
if __name__ == "__main__":
    main()