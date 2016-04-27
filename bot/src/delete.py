import settings
import logging
import telegram

from pymongo import MongoClient

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


def delete_alerts(bot, update):
    logger.info('delete_alerts // OK')
    client = MongoClient(settings.mongo_url)
    db = client.ShoudItakemyumbrellaBot
    where = {'chat_id': update.message.chat_id}
    data = {'$set': {'done': True}}
    db.alarms.update_many(where, data)
    bot.sendMessage(update.message.chat_id, text="Done {0}".format(telegram.Emoji.HEAVY_CHECK_MARK))
