import logging
import os.path
from abc import abstractmethod, ABC
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

from ..utils import generate_id_exports_url, save_id_data, extract_gz, get_data_ids

logger = logging.getLogger('data_downloader')


class BaseSpider(ABC, scrapy.Spider):
    allowed_domains = ["api.themoviedb.org", "files.tmdb.org"]
    languages_to_scrape = get_project_settings().get("LANGUAGES_TO_SCRAPE")

    @property
    @abstractmethod
    def content_type(self):
        pass

    @property
    @abstractmethod
    def details_url(self):
        pass

    def start_requests(self) -> Iterable[Request]:
        download_url = generate_id_exports_url(self.content_type)
        logger.debug(f"Downloading {self.content_type} ids data...")
        yield scrapy.Request(url=download_url, callback=self.download_ids_data)

    def download_ids_data(self, response):
        download_content = response.body
        store_location = get_project_settings().get('FILES_STORE')

        downloaded_filename = f"{self.content_type}_data.gz"
        data_filename = f"{self.content_type}_data.json"

        try:
            save_id_data(store_location, downloaded_filename, download_content)
            extract_gz(store_location, downloaded_filename, data_filename)
        except Exception as e:
            logger.error(f"Unexpected error occurred when downloading {self.content_type} ids data: {e}")
            raise CloseSpider(reason=f"Cannot download {self.content_type} data")
        logger.debug(f"Successfully downloaded {self.content_type} ids data")

        for content_id in get_data_ids(os.path.join(store_location, data_filename)):
            content_details_url = f"{self.details_url}{content_id}"
            yield scrapy.Request(url=content_details_url, callback=self.get_details)

    def get_details(self, response):
        raise NotImplementedError("This method should be overridden in derived classes")
