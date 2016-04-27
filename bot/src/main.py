#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import telegram
from telegram.ext import Updater
import logging
from pprint import pprint
import settings
#Import each handeler

from save_location import ALL
from get_weater import get_now
from start import start
from remind import start_remind, get_hour, set_alarm
from settings import normal_keyboard
from delete import delete_alerts

from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, RegexHandler
from telegram import KeyboardButton
from telegram.ext import filters
# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    logger.debug("Using {0} telegram key".format(settings.telegram_key))
    updater = Updater(settings.telegram_key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    dp.addHandler(start_handler)
    dp.addHandler(help_handler)


    all_handler = MessageHandler([filters.LOCATION], ALL)
    now_handler = RegexHandler("Should I take my umbrella today ?", get_now)
    start_handeler = RegexHandler("Remind me of my umbrella tomorrow", start_remind)
    delete_handeler = RegexHandler("Delete alerts", delete_alerts)

    dp.addHandler(all_handler)
    dp.addHandler(delete_handeler)
    tomorrow_handeler = RegexHandler("No, just tomorrow.", get_hour)
    everyday_handeler = RegexHandler("Yes, everyday !", get_hour)
    dp.addHandler(now_handler)
    dp.addHandler(start_handeler)

    dp.addHandler(tomorrow_handeler)
    dp.addHandler(everyday_handeler)

    hour_handeler = RegexHandler("\d+ am", set_alarm)
    dp.addHandler(hour_handeler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()