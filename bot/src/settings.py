import telegram
import os
from telegram import KeyboardButton
import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

user = ''
pw = ''
host = 'database'
port = 27017

user_str = ''
if user != '' and pw != '':
    user_str = "{user}:{pw}@".format(user=user,
                                     pw=pw)
mongo_url = 'mongodb://{user_str}{host}:{port}'.format(user_str=user_str,
                                                       host=host,
                                                       port=port)

telegram_key = os.environ.get('telegram_key', 'default')
weather_key = os.environ.get('weather_key', 'default')

if telegram_key == "default" or weather_key == "default":
    logger.error("API KEY MISSING FORM ENV")

logger.info("telegram_key = {0}".format(telegram_key))
logger.info("weather_key = {0}".format(weather_key))

normal_keyboard = telegram.ReplyKeyboardMarkup(
                    [[KeyboardButton('Should I take my umbrella today ?')],
                     [KeyboardButton('Remind me of my umbrella tomorrow')],
                     [KeyboardButton('Change location', request_location=True), KeyboardButton('Delete alerts')]]
                    )