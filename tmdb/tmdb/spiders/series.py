import scrapy

from .base_spider import BaseSpider
from ..items import TVSeriesItem, MovieAndSeriesTranslationItem, GenreItem
from ..utils import ContentType


class SeriesSpider(BaseSpider):
    name = "series"

    custom_settings = {
        "ITEM_PIPELINES": {
            "tmdb.pipelines.MediaItemPipeline": 300,
            "tmdb.pipelines.SaveMediaPipeline": 800
        }
    }

    @property
    def content_type(self):
        return ContentType.SERIES

    @property
    def details_url(self):
        return "https://api.themoviedb.org/3/tv/"

    def get_details(self, response):
        data = response.json()
        movie_item = TVSeriesItem()
        movie_item["id"] = data.get("id")
        movie_item["backdrop_path"] = data.get("backdrop_path")
        movie_item["genres"] = []
        movie_item["origin_country"] = data.get("origin_country")
        movie_item["original_title"] = data.get("original_name")
        movie_item["poster_path"] = data.get("poster_path")
        movie_item["release_date"] = data.get("first_air_date")
        movie_item["in_production"] = data.get("in_production")
        movie_item["number_of_episodes"] = data.get("number_of_episodes")
        movie_item["number_of_seasons"] = data.get("number_of_seasons")
        movie_item["status"] = data.get("status")
        movie_item["vote_average"] = data.get("vote_average")

        default_translation = MovieAndSeriesTranslationItem()
        default_translation["is_default"] = True
        default_translation["language"] = "en-US"
        default_translation["overview"] = data.get("overview")
        default_translation["title"] = data.get("name")

        movie_item["translations"] = [default_translation]

        for genre in data.get("genres"):
            genre_item = GenreItem()
            genre_item["id"] = genre["id"]
            movie_item["genres"].append(genre_item)

        for language in self.languages_to_scrape:
            url = f"{self.details_url}{movie_item['id']}?language={language}"
            yield scrapy.Request(url=url, callback=self.get_series_translations,
                                 meta={"item": movie_item, "language": language})

    def get_series_translations(self, response):
        movie_item = response.meta["item"]
        data = response.json()

        translation = MovieAndSeriesTranslationItem()
        translation["is_default"] = False
        translation["language"] = response.meta["language"]
        translation["overview"] = data.get("overview")
        translation["title"] = data.get("name")

        movie_item["translations"].append(translation)

        if len(movie_item["translations"]) == len(self.languages_to_scrape) + 1:
            yield movie_item
