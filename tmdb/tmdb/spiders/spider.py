from typing import Iterable, Any
from urllib.parse import urlencode

import scrapy
from scrapy import Request
from scrapy.http import Response


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["api.themoviedb.org"]
    api_url = "https://api.themoviedb.org/3/discover/movie?"
    max_page = 500
    params = {
        "include_adult": False,
        "include_video": False,
        "language": "en-US",
        "sort_by": "vote_count.desc"
    }

    def start_requests(self) -> Iterable[Request]:
        for i in range(self.max_page):
            params = self.params
            params["page"] = i + 1
            url = self.api_url + urlencode(params)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        data = response.json()
        results = data.get("results")
        if results:
            for result in results:
                yield result
