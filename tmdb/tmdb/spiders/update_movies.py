from .movie import MovieSpider
from .base_update_spider import BaseUpdateSpider


class UpdateMoviesSpider(BaseUpdateSpider, MovieSpider):
    name = "update_movies"

    @property
    def changes_url(self):
        return "https://api.themoviedb.org/3/movie/changes?"
