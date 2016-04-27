import requests
import pyowm
import pytz
from datetime import datetime, timedelta

from settings import weather_key, logger

def weater(lat, lng, timezone, unit='celsius', weather_key_=weather_key):
    res = {}
    try:
        owm = pyowm.OWM(weather_key_)
        observation = owm.three_hours_forecast_at_coords(lat, lng)
    except Exception, e:
        logger.error("weater {0}".format(e.message))
    rain = False
    now = datetime.now(pytz.timezone(timezone))
    for x in xrange(1, 13):
        working_time = now + timedelta(hours=x)
        if observation.will_be_rainy_at(working_time):
            rain = True
            break
    res['rain'] = rain
    tmp = observation.get_forecast()
    res['location'] = tmp.get_location().get_name()
    return res

if __name__ == '__main__':
    print weater(45.757753, 4.742274, unit='celsius')
    print weater(45.757753, 4.742274, unit='fahrenheit')
    print weater(31.2304, 121.4737, unit='celsius')
    print weater(21.0287, 105.8521, unit='celsius')

