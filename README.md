# ShouldItakemyumbrella_bot

This is the code for [@ShouldItakemyumbrella_bot](https://telegram.me/ShouldItakemyumbrella_bot) it is runing on a digital ocean instance.
It is uses [openweather](http://openweathermap.org/api) to get weather predictions.

# How to run

1. Install:
    - Docker
    - Docker-compose

2. Git clone this repo
    - `git clone https://github.com/sbres/ShouldItakemyumbrella_bot.git && cd ShouldItakemyumbrella_bot`

3. Edit `docker-compose.yml` and add your keys.
    - [openweathey api key](http://openweathermap.org/appid)
    - [Telegram api key](https://core.telegram.org/bots#6-botfather)

4. Run docker-compose
    - `docker-compose up`

Now the bot should build the images and be runing.
