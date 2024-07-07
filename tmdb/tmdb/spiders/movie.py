import logging
import os.path
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

from ..items import MovieItem, MovieTranslationItem, GenreItem
from ..utils import generate_id_exports_url, save_id_data, extract_gz, get_movie_ids

logger = logging.getLogger('data_downloader')


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["api.themoviedb.org", "files.tmdb.org"]

    movie_details_url = "https://api.themoviedb.org/3/movie/"
    languages_to_scrape = get_project_settings().get("LANGUAGES_TO_SCRAPE")

    custom_settings = {
        "ITEM_PIPELINES": {
            "tmdb.pipelines.MovieItemPipeline": 300,
            "tmdb.pipelines.SaveMoviesPipeline": 800
        }
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
            movie_details_url = f"{self.movie_details_url}{movie_id}"
            yield scrapy.Request(url=movie_details_url, callback=self.get_movie_details)

    def get_movie_details(self, response):
        # TODO: Add tv series support
        data = response.json()
        movie_item = MovieItem()
        movie_item["id"] = data.get("id")
        movie_item["backdrop_path"] = data.get("backdrop_path")
        movie_item["genres"] = []
        movie_item["origin_country"] = data.get("origin_country")
        movie_item["original_title"] = data.get("original_title")
        movie_item["poster_path"] = data.get("poster_path")
        movie_item["release_date"] = data.get("release_date")
        movie_item["runtime"] = data.get("runtime")
        movie_item["vote_average"] = data.get("vote_average")

        default_translation = MovieTranslationItem()
        default_translation["is_default"] = True
        default_translation["language"] = "en-US"
        default_translation["overview"] = data.get("overview")
        default_translation["title"] = data.get("title")

        movie_item["translations"] = [default_translation]

        for genre in data.get("genres"):
            genre_item = GenreItem()
            genre_item["id"] = genre["id"]
            movie_item["genres"].append(genre_item)

        for language in self.languages_to_scrape:
            url = f"{self.movie_details_url}{movie_item['id']}?language={language}"
            yield scrapy.Request(url=url, callback=self.get_movie_translations,
                                 meta={"item": movie_item, "language": language})

    def get_movie_translations(self, response):
        movie_item = response.meta["item"]
        data = response.json()

        translation = MovieTranslationItem()
        translation["is_default"] = False
        translation["language"] = response.meta["language"]
        translation["overview"] = data.get("overview")
        translation["title"] = data.get("title")

        movie_item["translations"].append(translation)

        if len(movie_item["translations"]) == len(self.languages_to_scrape) + 1:
            yield movie_item
