from .series import SeriesSpider
from .base_update_spider import BaseUpdateSpider


class UpdateSeriesSpider(BaseUpdateSpider, SeriesSpider):
    name = "update_series"

    @property
    def changes_url(self):
        return "https://api.themoviedb.org/3/tv/changes?"
