import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

model = genai.GenerativeModel(config.GEMINI_MODEL)

prompt = "Say hello, Gemini!"

try:
    response = model.generate_content(prompt)
    print("Gemini response:", response.text.strip())
except Exception as e:
    print("Gemini API error:", e)
