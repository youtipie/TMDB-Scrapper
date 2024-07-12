#!/bin/bash

spiders=("category" "movie" "series")

cd /app || exit

for spider in "${spiders[@]}"
do
    scrapy crawl "$spider"
done
