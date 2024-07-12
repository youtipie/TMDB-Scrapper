FROM python:slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends cron

RUN chmod u+x start_once_spiders.sh daily_spiders.sh run_cron.sh boot.sh

ADD crontab /etc/cron.d/crontab

ENTRYPOINT ["./boot.sh"]