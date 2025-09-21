import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    print("Attempting to call Gemini API...")
    response = model.generate_content("Hello")
    
    print("\nSuccess! API Response:")
    print(response.text)
    
except Exception as e:
    print(f"\nError occurred: {str(e)}")
    print("\nTroubleshooting steps:")
    print("1. Verify GEMINI_API_KEY in .env file")
    print("2. Check the key is valid in Google AI Studio")
    print("3. Ensure you've enabled the Gemini API in Google Cloud Console")
    print("4. Check your internet connection")
