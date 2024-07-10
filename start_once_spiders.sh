#!/bin/bash

spiders=("category" "movie" "series")

cd /tmdb
for spider in "${spiders[@]}"
do
    scrapy crawl "$spider"
done
