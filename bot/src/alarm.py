import telegram
import time
import pytz
import sys
import settings
from pymongo import MongoClient
from datetime import datetime
from get_weater_api import weater
from generators import create

def try_weather(bot, db, chat_id, weater_key, level=0):
    try:
        user_query = {'chat_id': chat_id}
        user_data = db.users.find(user_query)[0]
        w = weater(user_data['loc']['lat'], user_data['loc']['lng'], user_data['timezone'], weather_key_=weater_key)
        ret = create(w.get('rain'), w.get('location'))
        bot.sendMessage(chat_id, text=ret)
    except Exception, e:
        print 'Fuck try_weather // {0}'.format(e.message)
        if level > 10:
            return
        else:
            try_weather(bot, db, chat_id, weater_key, level=level + 1)
        time.sleep(1)

def main(telegram_key, weater_key):
    now = datetime.utcnow().hour
    print 'Allarm for {0}'.format(now)
    client = MongoClient(settings.mongo_url)
    db = client.ShoudItakemyumbrellaBot
    to_find = {'hour': now,
               'done': False}
    try:
        res = db.alarms.find(to_find)
    except Exception, e:
        print 'No one to alert'
    bot = telegram.Bot(token=telegram_key)
    for user in res:
        try_weather(bot, db, user['chat_id'], weater_key)
        if user['repeat'] == False:
            data = {'$set': {'done': True}}
            where = {"_id": user['_id']}
            db.alarms.update_one(where, data)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main(settings.telegram_key, settings.weather_key)
