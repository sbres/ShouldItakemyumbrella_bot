import random

def create(rain, city):
    if rain:
        ret = create_rain(city)
    else:
        ret = create_not_rain(city)
    return ret

def create_rain(city):
    sentences = ['Better take your umbrella. It\'s going to rain in {0}.']
    res = random.choice(sentences)
    return res.format(city)

def create_not_rain(city):
    sentences = ['It\'s not goint to rain in {0}']
    res = random.choice(sentences)
    return res.format(city)