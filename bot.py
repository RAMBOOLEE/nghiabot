import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Thay YOUR_TOKEN bằng mã token của bot Telegram
updater = Updater("7867490521:AAFprI8-_CQ4jl5tjYo6GVp_m9TycFKFSas", use_context=True)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello, I'm your bot!")

dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
