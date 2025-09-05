import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram.ext import Updater, MessageHandler, Filters
from config import TELEGRAM_TOKEN, CONFIDENCE_THRESHOLD, TOP_K
from bot.qa_engine import QABot

qa = QABot()

def handle_message(update, context):
    try:
        chat_type = update.message.chat.type
        query = update.message.text
        print(f"[{chat_type}] Received:", query)

        answer, confidence = qa.search(query, threshold=CONFIDENCE_THRESHOLD, top_k=TOP_K)
        print("Answer:", answer, "Confidence:", confidence)

        # Private chat → always reply
        if chat_type == "private":
            update.message.reply_text(answer)
        else:
            # Group chat → only reply if confident and valid
            if confidence >= CONFIDENCE_THRESHOLD and "I don't know" not in answer:
                update.message.reply_text(answer)
            else:
                # stay silent, no spam
                print("Skipped replying (low confidence or irrelevant).")

    except Exception as e:
        print("Error in handle_message:", e)
        if update.message.chat.type == "private":
            update.message.reply_text("❌ Sorry, an error occurred. Please try again later.")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
