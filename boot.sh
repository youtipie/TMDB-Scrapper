#!/bin/bash

chmod 0644 /etc/cron.d/crontab

touch /var/log/cron.log

if [ -n "$INITIAL_SCRAPING" ] && [ "$INITIAL_SCRAPING" -eq 1 ]; then
  ./start_once_spiders.sh
else
   echo "Skipping initial scraping."
fi

./run_cron.sh


cron && tail -f /var/log/cron.log