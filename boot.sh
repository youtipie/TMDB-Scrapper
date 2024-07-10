#!/bin/bash

# Set up a cron job
echo "0 12 * * * ./daily_spiders.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/daily_spiders
chmod 0644 /etc/cron.d/daily_spiders
crontab /etc/cron.d/daily_spiders

cron

./start_once_spiders.sh

# Keep the container running to allow cron to work
tail -f /var/log/cron.log
