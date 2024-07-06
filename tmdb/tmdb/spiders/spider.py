import logging
import os.path
from io import BytesIO
from os.path import join
from typing import Iterable, Any
from urllib.parse import urlencode

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from scrapy.utils.project import get_project_settings

from ..items import MovieItem
from ..utils import generate_id_exports_url, save_id_data, extract_gz, get_movie_ids

logger = logging.getLogger('data_downloader')


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["api.themoviedb.org", "files.tmdb.org"]

    movie_details_url = "https://api.themoviedb.org/3/movie/"
    movie_details_params = {
        "language": "en-US"
    }

    def start_requests(self) -> Iterable[Request]:
        download_url = generate_id_exports_url()
        logger.debug("Downloading movie ids data...")
        yield scrapy.Request(url=download_url, callback=self.download_ids_data)

    def download_ids_data(self, response):
        download_content = response.body
        store_location = get_project_settings().get('FILES_STORE')

        downloaded_filename = "data.gz"
        data_filename = "data.json"

        try:
            save_id_data(store_location, downloaded_filename, download_content)
            extract_gz(store_location, downloaded_filename, data_filename)
        except Exception as e:
            logger.error("Unexpected error occurred when downloading movie ids data: %s", e)
            raise CloseSpider(reason="Cannot download data")
        logger.debug("Successfully downloaded movies ids data")

        for movie_id in get_movie_ids(os.path.join(store_location, data_filename)):
            movie_details_url = f"{self.movie_details_url}{movie_id}?{urlencode(self.movie_details_params)}"
            yield scrapy.Request(url=movie_details_url, callback=self.get_movie_details)

    def get_movie_details(self, response):
        data = response.json()
        movie_item = MovieItem()
        movie_item["id"] = data.get("id")
        movie_item["backdrop_path"] = data.get("backdrop_path")
        movie_item["genres"] = data.get("genres")
        movie_item["origin_country"] = data.get("origin_country")
        movie_item["original_title"] = data.get("original_title")
        movie_item["overview"] = data.get("overview")
        movie_item["poster_path"] = data.get("poster_path")
        movie_item["release_date"] = data.get("release_date")
        movie_item["runtime"] = data.get("runtime")
        movie_item["title"] = data.get("title")
        movie_item["vote_average"] = data.get("vote_average")
        yield movie_item
