from typing import Any, Iterable

import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.utils.project import get_project_settings

from ..items import GenreItem


class CategorySpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["api.themoviedb.org"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "tmdb.pipelines.GenreItemPipeline": 300,
            "tmdb.pipelines.SaveGenresPipeline": 800
        }
    }

    def start_requests(self) -> Iterable[Request]:
        languages = ["en-US"] + get_project_settings().get("LANGUAGES_TO_SCRAPE")
        for language in languages:
            url = f"https://api.themoviedb.org/3/genre/movie/list?language={language}"
            yield scrapy.Request(url=url, callback=self.parse, meta={"language": language})

    def parse(self, response: Response, **kwargs: Any) -> Any:
        data = response.json()
        lang = response.meta["language"]
        genres = data.get("genres")

        for genre in genres:
            genre_item = GenreItem()
            genre_item["id"] = genre["id"]
            genre_item["is_default"] = lang == "en-US"
            genre_item["language"] = lang
            genre_item["name"] = genre["name"]
            yield genre_item
