import os
import google.generativeai as genai

# Get your Gemini API key
# It's highly recommended to store your API key in an environment variable
# named GEMINI_API_KEY for security.
GEMINI_API_KEY = "AIzaSyC6yq-rurP5HXIK5PJ0jjmM16NIuQvk4jo"

if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY not found. Please set it in your .env file or as an environment variable.")
    exit()

# Configure the Gemini API with your key
genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Listing available Gemini models...")
print("-----------------------------------")

try:
    # Iterate through all available models
    for m in genai.list_models():
        # Only print models that can generate content (e.g., text, code)
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
            print(f"  Description: {m.description}")
            print(f"  Input Token Limit: {m.input_token_limit}")
            print(f"  Output Token Limit: {m.output_token_limit}")
            print(f"  Supported Methods: {m.supported_generation_methods}")
            print("-" * 35)

except Exception as e:
    print(f"❌ An error occurred while fetching models: {e}")
    print("Please ensure your API key is correct and has the necessary permissions.")
    print("You might also need to update your 'google-generativeai' package:")
    print("pip install --upgrade google-generativeai")

print("\n✅ Model listing complete.")
