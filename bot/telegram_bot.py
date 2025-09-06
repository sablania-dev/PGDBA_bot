import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from config import TELEGRAM_TOKEN, CONFIDENCE_THRESHOLD, TOP_K
from bot.qa_engine import QABot

import asyncio

# Flask app
app = Flask(__name__)

# Telegram application
application = Application.builder().token(TELEGRAM_TOKEN).build()
qa = QABot()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        chat_type = update.message.chat.type
        query = update.message.text
        print(f"[{chat_type}] Received:", query)

        answer, confidence = qa.search(query, threshold=CONFIDENCE_THRESHOLD, top_k=TOP_K)
        print("Answer:", answer, "Confidence:", confidence)

        if chat_type == "private":
            # Always reply in DMs
            await update.message.reply_text(answer)
        else:
            # Group chat → only reply if confident & not irrelevant
            if confidence >= CONFIDENCE_THRESHOLD and "I don't know" not in answer:
                await update.message.reply_text(answer)
            else:
                print("Skipped replying (low confidence or irrelevant).")

    except Exception as e:
        print("Error in handle_message:", e)
        if update.message and update.message.chat.type == "private":
            await update.message.reply_text("❌ Sorry, an error occurred. Please try again later.")

# Add handler
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask route for webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
    except Exception as e:
        print("Webhook error:", e)
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render will set PORT
    app.run(host="0.0.0.0", port=port)
