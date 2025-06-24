import os
import google.generativeai as genai
from datetime import datetime

GEMINI_API_KEY = "AIzaSyAaUej3CVIVz68H_v-GowFcpdvzIogOiVw"

# ========== 🔧 GEMINI SETUP ==========
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        top_p=1,
        top_k=1,
        max_output_tokens=2048,
    )
)

# ========== 🤖 GEMINI PROMPT ==========
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

# ========== 📝 LOGGING FUNCTION ==========
def log_change(path, old_code, new_code, reason):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_prompt = (
        f"Explain what was changed in the following Python code:\n\n"
        f"Old Code:\n{old_code[:1000]}\n\nNew Code:\n{new_code[:1000]}"
    )
    explanation = gemini_prompt(change_prompt).strip()
    log_entry = (
        f"🕒 {timestamp}\n"
        f"📄 File: {path}\n"
        f"🔄 Reason: {reason}\n"
        f"🧠 Changes:\n{explanation}\n"
        f"{'-'*40}\n"
    )
    file_path = path+"/log.txt"
    
    if os.path.exist:
    	with open(file_path, "a", encoding="utf-8") as log_file:
     	   log_file.write(log_entry)
    else:
    	with open(file_path, "w", encoding="utf-8") as log_file:
    		log_file.write(log_entry)

# ========== 🧠 AI PROCESSING ==========
def correct_errors_with_gemini(code):
    prompt = f"Fix the following Python code. Return corrected and formatted Python code only:\n\n{code} and if you don't find error then give code as it is"
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

# ========== 🧪 TESTING & RUNNING ==========
def test_project(folder):
    print("\n🧪 Running all .py files for testing...")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                print(f"\n▶️ Testing: {path}")
                result = os.system(f"python \"{path}\"")
                if result != 0:
                    print(f"❌ Error occurred in: {file}")
                else:
                    print(f"✅ Passed: {file}")

def run_project(folder):
    print("\n▶️ Running main project file...")
    main_file = os.path.join(folder, "main.py")
    if os.path.exists(main_file):
        os.system(f"python \"{main_file}\"")
    else:
        print("❌ No 'main.py' found in project folder.")

def start_project(folder):
    print("\n🚀 Starting project and checking for known ports...")
    possible_files = ["app.py", "main.py", "manage.py"]
    entry_point = None
    for f in possible_files:
        path = os.path.join(folder, f)
        if os.path.exists(path):
            entry_point = path
            break

    if entry_point:
        print(f"▶️ Starting: {entry_point}")
        os.system(f"python \"{entry_point}\"")
    else:
        print("❌ No known entry point found.")

# ========== 🚀 MAIN ==========
def main():
    print("🔧 Gemini Code Assistant")
    project_folder, algo_file = get_project_and_algo_paths()

    manual_error = input("\n📝 Optional: Paste any error message you'd like Gemini to fix (or leave blank):\n> ").strip()
    clarify_prompt = input("💬 Optional: Add any clarifying instruction to guide Gemini (or leave blank):\n> ").strip()

    print("\n🔍 Reading Python files...")
    python_files = read_python_files(project_folder)

    for path, code in python_files.items():
        print(f"\n📄 Fixing: {path}")
        if manual_error:
            fixed_code = correct_with_manual_error(code, manual_error, clarify_prompt)
            reason = "Manual Error Fix"
        else:
            fixed_code = correct_errors_with_gemini(code)
            reason = "Auto Error Correction"

        if fixed_code.strip():
            fixed_code = "#" + fixed_code.replace("```", "")
            write_file(path, fixed_code)
            log_change(path, code, fixed_code, reason)
            print(f"✅ Overwritten: {path}")
        else:
            print(f"⚠️ No response from Gemini. File not updated: {path}")

    confirm_gen = input("\n🧠 Do you want to generate Python code from the algorithm file? (y/n): ").strip().lower()
    if confirm_gen == 'y':
        new_code = generate_code_from_algorithm(algo_file)
        filename = input("📄 Enter filename to save (e.g., main.py): ").strip()
        save_path = project_folder
        write_file(save_path, new_code)
        log_change(save_path, "", new_code, "Generated from Algorithm")
        print(f"✅ Generated code saved to: {save_path}")
    else:
        print("🛑 Skipped code generation.")

    print("\n📂 Files in project folder:")
    for file in list_all_files(project_folder):
        print(" -", file)

    print("\n📦 Additional Actions:")
    print("1. 🧪 Test all Python files")
    print("2. ▶️ Run main.py")
    print("3. 🚀 Start project (detect Flask/Django/FastAPI)")
    choice = input("Select action (1/2/3 or Enter to skip): ").strip()

    if choice == "1":
        test_project(project_folder)
    elif choice == "2":
        run_project(project_folder)
    elif choice == "3":
        start_project(project_folder)
    else:
        print("✅ No additional action selected.")

# ========== 🔧 RUN ==========
if __name__ == "__main__":
    main()