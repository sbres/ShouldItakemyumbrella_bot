import settings
import logging

from geopy import geocoders
from pymongo import MongoClient
from settings import normal_keyboard

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

def ALL(bot, update):
    if update.message.location is not None:
        save_location(update)
        bot.sendMessage(update.message.chat_id, text='Got it !', reply_markup=normal_keyboard)


def save_location(update):
    lat = update.message.location['latitude']
    lng = update.message.location['longitude']
    try:
        g = geocoders.GoogleV3()
        timezone = g.timezone((lat, lng))
        chat_id = update.message.chat_id
        to_insert = {'chat_id': chat_id,
                     'loc': {'lat': lat,
                             'lng': lng},
                     'timezone': str(timezone)
                     }
        logger.info('mongo_url {0}'.format(settings.mongo_url))
        client = MongoClient(settings.mongo_url)
        db = client.ShoudItakemyumbrellaBot
        db.users.insert_one(to_insert)
    except Exception, e:
        logger.warn('Update "%s" caused error "%s"' % (update, e.message))


