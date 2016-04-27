import settings
import logging
import random

from pymongo import MongoClient
from get_weater_api import weater
from generators import create
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

def get_now(bot, update):
    bot.sendMessage(update.message.chat_id, text='Let me go outside and check.')
    chat_id = update.message.chat_id
    try:
        to_find = {'chat_id': chat_id,
                     }
        client = MongoClient(settings.mongo_url)
        db = client.ShoudItakemyumbrellaBot
        try:
            res = db.users.find(to_find)[0]
        except Exception, e:
            logger.error('No location found // {0}'.format(e.message))
            bot.sendMessage(update.message.chat_id, text='You should save your location first')
            return
        w = weater(res['loc']['lat'], res['loc']['lng'], res['timezone'])
        ret = create(w.get('rain'), w.get('location'))
        bot.sendMessage(update.message.chat_id, text=ret)
    except Exception, e:
        logger.error('Update {0} caused error {1}'.format(update, e.message))



