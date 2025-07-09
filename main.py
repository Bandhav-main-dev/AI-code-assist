# streamlit_gemini_app.py
import streamlit as st
import os
import tempfile
import google.generativeai as genai
from datetime import datetime

# ========== 🔑 API KEY SETUP ==========
GEMINI_API_KEY = "AIzaSyAmPDi5PN5WgOgxBfolcV0tmS-HPtUSeXE"  # Replace with your actual API key
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
        return f"❌ Gemini Error: {e}"

# ========== FILE UTILITIES ==========
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

# ========== 📝 LOGGING FUNCTIONALITY ==========
def log_change(file_name, original_code, fixed_code):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = (
        f"Explain what was changed in the following Python code:\n\n"
        f"Old Code:\n{original_code[:1000]}\n\nNew Code:\n{fixed_code[:1000]}"
    )
    explanation = gemini_prompt(prompt)

    log_entry = (
        f"🕒 {timestamp}\n"
        f"📄 File: {file_name}\n"
        f"🧠 Changes:\n{explanation}\n"
        f"{'-'*40}\n"
    )
    with open("logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

# ========== AI FIX FUNCTIONS ==========
def correct_errors_with_gemini(code):
    prompt = f"Fix the following Python code. Return corrected and formatted Python code only:\n\n{code}\nIf no error, return the same code."
    return gemini_prompt(prompt)

def correct_with_manual_error(code, user_error, user_prompt=""):
    prompt = (
        "You are a Python code assistant."
        f"\nThe user reported the following error:\n{user_error}\n"
        f"\nFix this code:\n{code}\n"
        f"\nInstructions:\n{user_prompt}"
    )
    return gemini_prompt(prompt)

def generate_code_from_algorithm(algorithm_text):
    prompt = f"Convert the following algorithm into one or more working Python files. If multiple files are needed, separate them clearly by filename and code:\n\n{algorithm_text}"
    return gemini_prompt(prompt)

# ========== STREAMLIT APP ==========
st.title("🧠 Gemini Code Fixer & Generator")

mode = st.radio("Select Mode", ["Fix Code", "Generate from Algorithm"])

if mode == "Fix Code":
    uploaded_files = st.file_uploader("📤 Upload Python Files", accept_multiple_files=True, type=[".py"])
    manual_error = st.text_area("🔍 Optional: Error Message")
    user_instruction = st.text_area("🗒️ Optional: Additional Instructions")

    if st.button("🔧 Fix Code"):
        if not uploaded_files:
            st.warning("Please upload at least one Python (.py) file.")
        else:
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                code = file_bytes.decode("utf-8")
                st.subheader(f"📄 Fixing: {uploaded_file.name}")

                if manual_error.strip():
                    fixed_code = correct_with_manual_error(code, manual_error, user_instruction)
                else:
                    fixed_code = correct_errors_with_gemini(code)

                st.code(fixed_code, language='python')

                log_change(uploaded_file.name, code, fixed_code)

                st.download_button(
                    label=f"📥 Download Fixed {uploaded_file.name}",
                    data=fixed_code,
                    file_name=f"fixed_{uploaded_file.name}",
                    mime="text/plain"
                )

elif mode == "Generate from Algorithm":
    st.subheader("🧠 Paste Algorithm to Generate Python Code")
    algo_text = st.text_area("🧮 Enter your algorithm here")

    if st.button("🚀 Generate Code"):
        if not algo_text.strip():
            st.warning("Please paste an algorithm first.")
        else:
            result = generate_code_from_algorithm(algo_text)

            files = {}
            current_file = None
            lines = result.splitlines()
            for line in lines:
                if line.strip().endswith(".py") and ".py" in line.lower():
                    current_file = line.strip().replace("`", "")
                    files[current_file] = ""
                elif current_file:
                    files[current_file] += line + "\n"

            if not files:
                st.code(result, language='python')
                st.download_button(
                    label=f"📥 Download generated_code.py",
                    data=result,
                    file_name="generated_code.py",
                    mime="text/plain"
                )
            else:
                output_dir = "generated_files"
                os.makedirs(output_dir, exist_ok=True)
                for filename, code in files.items():
                    file_path = os.path.join(output_dir, filename)
                    write_file(file_path, code)
                    st.subheader(f"📄 {filename}")
                    st.code(code, language='python')
                    st.download_button(
                        label=f"📥 Download {filename}",
                        data=code,
                        file_name=filename,
                        mime="text/plain"
                    )

# ========== TOGGLE LAST CHANGE LOG VIEW ==========
if 'show_log' not in st.session_state:
    st.session_state['show_log'] = False

if st.button("🕒 Toggle Last Change Log"):
    st.session_state['show_log'] = not st.session_state['show_log']

if st.session_state['show_log']:
    if os.path.exists("logs.txt"):
        with open("logs.txt", "r", encoding="utf-8") as log_file:
            logs = log_file.read().strip().split("----------------------------------------")
            last_log = logs[-2] if len(logs) > 1 else logs[0]
            st.text_area("📑 Last Change Log", last_log.strip(), height=300)
    else:
        st.warning("No log file found.")