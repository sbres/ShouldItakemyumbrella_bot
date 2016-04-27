#!/bin/bash
set -e;

echo "01 * * * * /usr/local/bin/python /work/alarm.py $telegram_key $weather_key \
 >> /var/log/myjob.log 2>&1" | crontab -u root -;

cron;

/usr/local/bin/python /work/main.py;
