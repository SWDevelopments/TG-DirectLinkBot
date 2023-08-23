import os
import logging
from telegram import Update, ParseMode
from telegram.ext import (
    CallbackContext,
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

# Access the environment variables
TOKEN = os.getenv("TG_Token")
FEEDBACK_CHANNEL_ID = os.getenv("CH_Token")


def start(update: Update, context: CallbackContext):
    """Handler for the /start command"""
    update.message.reply_text("Hi! Send me any file or files, and I'll provide direct download links for them.")


def help(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    help_text = """
    Here are the available commands:

    /start - Start the bot
    /help - Show help message
    """
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


def handle_file(update: Update, context: CallbackContext):
    """Handler for file uploads"""
    try:
        file_list = update.message.document
        file_links = []
        for file in file_list:
            file_id = file.file_id
            file_name = file.file_name
            file_size = file.file_size
            direct_link = f'https://api.telegram.org/file/bot{TOKEN}/{file_id}/{quote(file_name)}'
            file_link = f"File: {file_name}\nSize: {file_size} bytes\n\nDirect Link: {direct_link}"
            file_links.append(file_link)

        response = "\n\n".join(file_links)
        update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logging.error(f"An error occurred while handling the file upload: {str(e)}")
        update.message.reply_text("Oops! Something went wrong. Please try again later.")


def feedback(update: Update, context: CallbackContext):
    """Handler for feedback"""
    user = update.effective_user
    feedback_text = update.message.text
    response = "Thank you for your feedback!"
    message_text = f"[Feedback]\nUser ID: {user.id}\nUsername: {user.username or 'Not Available'}\nMessage: {feedback_text}"
    context.bot.send_message(chat_id=FEEDBACK_CHANNEL_ID, text=message_text, parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(response)


def log_message(update: Update, context: CallbackContext):
    """Handler for all messages to log them"""
    user = update.effective_user
    message = update.effective_message
    log_text = f"[Log]\nUser ID: {user.id}\nUsername: {user.username or 'Not Available'}\nMessage: {message.text}"
    context.bot.send_message(chat_id=FEEDBACK_CHANNEL_ID, text=log_text, parse_mode=ParseMode.MARKDOWN)


def unknown(update: Update, context: CallbackContext):
    """Handler for unknown commands"""
    update.message.reply_text("Sorry, I didn't understand that command. Use /help to see the list of available commands.")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, feedback))
    dp.add_handler(MessageHandler(Filters.all, log_message))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
