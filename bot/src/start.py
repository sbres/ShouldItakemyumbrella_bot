import telegram

from telegram import KeyboardButton
from pymongo import MongoClient
from settings import normal_keyboard, mongo_url
import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)



WELCOME_MESSAGE = "Hey nice to meet you. \n"\
                  "I'm ShouldItakemyumbrella_bot i will help you to never forget your umbrella.\n" \
                  "You can find my code here: https://github.com/sbres/ShouldItakemyumbrella_bot\n\n" \
                  "It seems I don't know you !\n"\
                  "Tell me, Where are you from ?"

BACK_MESSAGE = "Welcome back I missed you !"

import time

def start(bot, update):
    client = MongoClient(mongo_url)
    db = client.ShoudItakemyumbrellaBot
    try:
        res = db.users.find({'chat_id': update.message.chat_id})
        res = res.count()

    except Exception, e:
        logger.error("{0}".format(e))
        keyboard = telegram.ReplyKeyboardMarkup([[KeyboardButton('Save location', request_location=True)]])
        bot.sendMessage(update.message.chat_id, text=WELCOME_MESSAGE, reply_markup=keyboard)
        return
    if res == 0:
        keyboard = telegram.ReplyKeyboardMarkup([[KeyboardButton('Save location', request_location=True)]])
        bot.sendMessage(update.message.chat_id, text=WELCOME_MESSAGE, reply_markup=keyboard)
    else:
        bot.sendMessage(update.message.chat_id, text=BACK_MESSAGE, reply_markup=normal_keyboard)
