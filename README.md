# PGDBA Admissions FAQ Bot

A conversational AI assistant for answering PGDBA admissions questions via Telegram and web, using context-aware retrieval and Gemini/OpenAI LLMs.

## Features
- **Telegram Bot**: Responds to user queries in private and group chats.
- **Web API**: Endpoint for website chatbot integration.
- **Contextual Retrieval**: Uses FAISS and sentence-transformers for semantic search over a curated context document.
- **LLM Synthesis**: Answers are generated using Gemini (Google) or OpenAI models, grounded in the provided context.
- **Configurable**: Easily switch models, thresholds, and API keys in `config.py`.

## Project Structure
```
PGDBA_bot/
├── build_index.py           # Build FAISS index from context
├── config.py                # API keys and settings (DO NOT COMMIT)
├── requirements.txt         # Python dependencies
├── test_gemini.py           # (Optional) Gemini API test script
├── bot/
│   ├── qa_engine.py         # Core retrieval and LLM logic
│   ├── telegram_bot.py      # Telegram bot entrypoint
│   └── web_api.py           # (Optional) Web API for chatbot
├── data/
│   ├── context_document.txt # Main context for retrieval
│   ├── faqs.json            # (Optional) FAQ data
│   └── course_list.png      # (Optional) Course info
├── models/
│   └── embeddings_index.faiss # FAISS index (generated)
├── frontend/
│   ├── chatbot_widget.html  # (Optional) Web widget
│   └── chatbot_widget.js    # (Optional) Widget JS
└── ...
```

## Setup
1. **Clone the repo**
2. **Install dependencies**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure API keys**
   - Edit `config.py` with your Telegram, OpenAI, and Gemini API keys.
    - Set Telegram and Gemini API Keys as environment variables:
       - **Windows (PowerShell):**
          ```powershell
          $env:TELEGRAM_TOKEN="<your-telegram-token>"
          $env:GEMINI_API_KEY="<your-gemini-api-key>"
          ```
       - **Linux/macOS (bash):**
          ```bash
          export TELEGRAM_TOKEN="<your-telegram-token>"
          export GEMINI_API_KEY="<your-gemini-api-key>"
          ```
       Replace `<your-telegram-token>` and `<your-gemini-api-key>` with your actual keys.
4. **Prepare context**
   - Edit `data/context_document.txt` with your FAQ/context.
   - Run the index builder:
     ```powershell
     python build_index.py
     ```
5. **Run the Telegram bot**
   ```powershell
   python -m bot.telegram_bot
   ```

## Usage
- **Telegram**: Chat with your bot (add it via BotFather, use your token).
- **Web API**: (If enabled) Integrate with your website using the provided endpoint.

## Security
- Never commit `config.py` or API keys.
- Use `.gitignore` to exclude sensitive files and model/data outputs.

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies.

## Credits
- Built with [sentence-transformers](https://www.sbert.net/), [FAISS](https://github.com/facebookresearch/faiss), [python-telegram-bot](https://python-telegram-bot.org/), [Google Generative AI](https://ai.google.dev/), and [OpenAI](https://openai.com/).
- Developed by Sarthak Sablania, PGDBA Batch-10 (2024-26)

---

For questions or contributions, open an issue or pull request.
