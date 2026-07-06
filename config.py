# config.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Read Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")