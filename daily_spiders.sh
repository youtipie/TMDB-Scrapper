#!/bin/bash

spiders=("update_movies" "update_series")

cd /tmdb
for spider in "${spiders[@]}"
do
    scrapy crawl "$spider"
done
