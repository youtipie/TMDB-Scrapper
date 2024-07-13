import logging
import os.path
from abc import abstractmethod, ABC
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings

from ..utils import get_data_ids, get_data_filename

logger = logging.getLogger('data_downloader')


class BaseSpider(ABC, scrapy.Spider):
    allowed_domains = ["api.themoviedb.org", "files.tmdb.org"]
    languages_to_scrape = get_project_settings().get("LANGUAGES_TO_SCRAPE")
    store_location = get_project_settings().get("FILES_STORE")

    @property
    @abstractmethod
    def content_type(self):
        pass

    @property
    @abstractmethod
    def details_url(self):
        pass

    def __init__(self):
        super().__init__()
        self.data_filename = get_data_filename(self.content_type)

    def start_requests(self) -> Iterable[Request]:
        for content_id in get_data_ids(os.path.join(self.store_location, self.data_filename)):
            content_details_url = f"{self.details_url}{content_id}"
            yield scrapy.Request(url=content_details_url, callback=self.get_details)

    def get_details(self, response):
        raise NotImplementedError("This method should be overridden in derived classes")
