from abc import abstractmethod
from typing import Iterable

import scrapy
from scrapy import Request

from .base_spider import BaseSpider


class BaseUpdateSpider(BaseSpider):

    @property
    @abstractmethod
    def changes_url(self):
        pass

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(url=self.changes_url + "page=1", callback=self.get_changed_media)

    def get_changed_media(self, response):
        data = response.json()

        page = data.get("page")
        total_pages = data.get("total_pages")

        for item in data.get("results"):
            details_url = f"{self.details_url}{item.get('id')}"
            yield scrapy.Request(url=details_url, callback=self.get_details)

        if page < total_pages:
            page += 1
            next_page_url = f"{self.changes_url}page={page}"
            yield scrapy.Request(url=next_page_url, callback=self.get_changed_media)
