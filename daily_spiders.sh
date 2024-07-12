#!/bin/bash

spiders=("update_movies" "update_series")

cd /app || exit

for spider in "${spiders[@]}"
do
    scrapy crawl "$spider"
done
