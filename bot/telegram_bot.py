import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from config import TELEGRAM_TOKEN, CONFIDENCE_THRESHOLD, TOP_K
from bot.qa_engine import QABot

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

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
