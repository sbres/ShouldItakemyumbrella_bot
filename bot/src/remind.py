import telegram
import pytz
import settings
from datetime import datetime, timedelta

from telegram import KeyboardButton
from settings import normal_keyboard
from pymongo import MongoClient
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start_remind(bot, update):
    to_find = {'chat_id': update.message.chat_id,
                     }
    client = MongoClient(settings.mongo_url)
    db = client.ShoudItakemyumbrellaBot
    try:
        res = db.users.find(to_find)[0]
    except Exception, e:
        bot.sendMessage(update.message.chat_id, text='You should save your location first')
        return
    custom_keyboard = [[KeyboardButton('No, just tomorrow.')],
                       [KeyboardButton('Yes, everyday !')]]
    keyboard = telegram.ReplyKeyboardMarkup(custom_keyboard)
    message = 'Do you want me to alert you everyday ?'
    bot.sendMessage(update.message.chat_id, text=message, reply_markup=keyboard)

def get_hour(bot, update):
    custom_keyboard = [[], []]
    if update.message.text == "No, just tomorrow.":
        #Just one time
        message = "Ok, What hour tomorrow ?"
        hour = '{0} am'
    else:
        #everyday
        message = "Cool, What hour ?"
        hour = '{0} am.'
    for x in xrange(6, 9):
        custom_keyboard[0].append(KeyboardButton(hour.format(x)))
    for x in xrange(9, 12):
        custom_keyboard[1].append(KeyboardButton(hour.format(x)))
    keyboard = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(update.message.chat_id, text=message, reply_markup=keyboard)

def set_alarm(bot, update):
    dot = update.message.text[-1:]
    if dot == ".":
        repeat = True
        hour = int(update.message.text[:-4])
    else:
        repeat = False
        hour = int(update.message.text[:-3])
    client = MongoClient(settings.mongo_url)
    db = client.ShoudItakemyumbrellaBot
    to_find = {'chat_id': update.message.chat_id}
    try:
        res = db.users.find(to_find)[0]
    except Exception, e:
        bot.sendMessage(update.message.chat_id, text='You should save your location first')
        return
    timezone = res.get('timezone')
    now = datetime.now(pytz.timezone(timezone))
    alarm = now
    alarm = alarm.replace(hour=hour, minute=00, second=00)
    if now > alarm:
        alarm = now + timedelta(days=1)
    alarm = alarm.astimezone(pytz.utc)
    alarm = {
        'hour': alarm.hour,
        'chat_id': update.message.chat_id,
        'repeat': repeat,
        'done': False
    }
    db.alarms.insert_one(alarm)
    bot.sendMessage(update.message.chat_id, text='Noted !', reply_markup=normal_keyboard)