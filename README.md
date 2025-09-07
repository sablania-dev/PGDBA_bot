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
4. **Run the Telegram bot**
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
# PGDBA Admissions FAQ Chatbot

A conversational AI assistant for answering PGDBA admissions questions via Telegram and web, using context-aware retrieval and Gemini LLM.

## Features
- **Telegram Bot**: Responds to user queries in private and group chats.
- **Contextual Retrieval**: Uses sentence-transformers and semantic search over a curated context document.
- **LLM Synthesis**: Answers are generated using Gemini (Google) LLM, grounded in the provided context.
- **Configurable**: Easily switch models, thresholds, and API keys in `config.py`.

## How It Works
1. **User sends a query** via Telegram or web.
2. **Query Embedding**: The query is embedded using a sentence-transformer model (default: `all-MiniLM-L6-v2`).
3. **Context Retrieval**: The embedding is compared to the first line of each paragraph (chunk) in `data/context_document.txt` using cosine similarity.
4. **Threshold Filtering**: Only chunks with similarity score ≥ `CONFIDENCE_THRESHOLD` (default: 0.3) are considered relevant.
5. **LLM Prompt Construction**: The top relevant chunks are combined into a prompt for Gemini.
6. **LLM Answer Generation**: Gemini generates an answer using the provided context. The answer is always printed as `[DEBUG]` in logs.
7. **Response Handling**:
   - If no chunk is above threshold, the bot replies: "I don't know based on the available context."
   - If at least one chunk is above threshold, the LLM's answer is sent to the user.

## Final Prompt Template
```
You are Kshitish The Chatbot, a PGDBA admissions FAQ assistant, made to help prospective students. Try to use the provided context to answer as much as possible. You don't have to use all of it, just what seems relevant. If the context does not contain the answer, respond exactly with: 'I don't know based on the available context.'
USER QUESTION: {user_query}

CONTEXT:
{context}
```

## LLM Used
- **Gemini** (Google Generative AI)
- Model: `gemini-1.5-flash` (configurable in `config.py`)

## Project Structure
```
PGDBA_bot/
├── build_index.py           # Build FAISS index from context
├── config.py                # API keys and settings
├── requirements.txt         # Python dependencies
├── bot/
│   ├── qa_engine.py         # Core retrieval and LLM logic
│   ├── telegram_bot.py      # Telegram bot entrypoint
│   └── web_api.py           # (Optional) Web API for chatbot
├── data/
│   ├── context_document.txt # Main context for retrieval
│   └── ...
├── models/
│   └── embeddings_index.faiss # FAISS index (generated)
└── ...
```

## Setup
1. **Clone the repo**
2. **Create and activate a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install "tzlocal<3.0" "apscheduler==3.10.4" pytz
   ```
4. **Configure API keys**
   - Edit `config.py` with your Telegram and Gemini API keys.
5. **Prepare context**
   - Edit `data/context_document.txt` with your FAQ/context.
   - Run the index builder:
     ```powershell
     python build_index.py
     ```
6. **Run the Telegram bot**
   ```powershell
   python -m bot.telegram_bot
   ```

## Security
- Never commit `config.py` or API keys to version control.
- Use `.gitignore` to exclude sensitive files and model/data outputs.

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies.

## Credits
- Built with [sentence-transformers](https://www.sbert.net/), [FAISS](https://github.com/facebookresearch/faiss), [python-telegram-bot](https://python-telegram-bot.org/), [Google Generative AI](https://ai.google.dev/).
- Developed by Sarthak Sablania, PGDBA Batch-10 (2024-26)

---

For questions or contributions, open an issue or pull request.
