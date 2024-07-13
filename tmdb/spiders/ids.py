import logging
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

from ..utils import generate_id_exports_url, save_id_data, extract_gz, get_data_filename, ContentType

logger = logging.getLogger('data_downloader')


class IdsSpider(scrapy.Spider):
    name = "ids"
    allowed_domains = ["files.tmdb.org"]
    store_location = get_project_settings().get("FILES_STORE")

    def start_requests(self) -> Iterable[Request]:
        for content_type in [ContentType.MOVIE, ContentType.SERIES]:
            download_url = generate_id_exports_url(content_type)
            logger.debug(f"Downloading {content_type} ids data...")
            yield scrapy.Request(url=download_url, callback=self.download_ids_data, meta={"content_type": content_type})

    def download_ids_data(self, response):
        download_content = response.body
        content_type = response.meta.get("content_type")
        downloaded_filename = f"{content_type}_data.gz"

        data_filename = get_data_filename(content_type)

        try:
            save_id_data(self.store_location, downloaded_filename, download_content)
            extract_gz(self.store_location, downloaded_filename, data_filename)
        except Exception as e:
            logger.error(f"Unexpected error occurred when downloading {content_type} ids data: {e}")
            raise CloseSpider(reason=f"Cannot download {content_type} data")
        logger.debug(f"Successfully downloaded {content_type} ids data")
