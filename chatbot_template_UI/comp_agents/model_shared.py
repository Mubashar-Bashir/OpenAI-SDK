# shared.py
from agents.extensions.models.litellm_model import LitellmModel
import os

# Load environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL") or "gemini/gemini-2.0-flash"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

if not MODEL:
    raise ValueError("MODEL is not set. Please ensure it is defined in your .env file.")

# Create LitellmModel instance
litellm_model = LitellmModel(
    model=MODEL,
    api_key=GEMINI_API_KEY
)