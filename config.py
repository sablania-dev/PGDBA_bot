# config.py

import os
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 🔹 Core Variables
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Change to larger/more accurate models if needed
CONFIDENCE_THRESHOLD = 0.3            # Lowered for better recall
TOP_K = 4                             # More context for Gemini

# Gemini API Key and Model
GEMINI_MODEL = "gemini-1.5-flash"  # Or whichever Gemini model you want to use