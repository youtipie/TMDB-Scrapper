FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY tmdb tmdb
COPY boot.sh start_once_spiders.sh daily_spiders.sh ./
RUN chmod +x start_once_spiders.sh daily_spiders.sh boot.sh

RUN apt-get update && apt-get install -y cron


ENTRYPOINT ["./boot.sh"]
