#!/bin/bash

chmod 0644 /etc/cron.d/crontab

touch /var/log/cron.log

./start_once_spiders.sh

./run_cron.sh

cron && tail -f /var/log/cron.log