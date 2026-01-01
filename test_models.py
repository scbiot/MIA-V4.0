import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

# List available models
print("Modelos disponibles:")
print("=" * 50)
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✓ {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description[:100]}...")
        print()
