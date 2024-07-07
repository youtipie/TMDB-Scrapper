from typing import Iterable

import scrapy
from scrapy import Request

from .movie import MovieSpider


# Inheriting the movie spider because it already has all the tools to scrape individual movie
# And in this spider we can just override start_requests to fetch updates from tmdb api
class UpdateMovieSpider(MovieSpider):
    name = "update_movie"
    movie_changes_url = "https://api.themoviedb.org/3/movie/changes?"

    def start_requests(self) -> Iterable[Request]:
        url = f"{self.movie_changes_url}page=1"
        yield scrapy.Request(url=url, callback=self.get_changed_movies)

    def get_changed_movies(self, response):
        data = response.json()

        page = data.get("page")
        total_pages = data.get("total_pages")

        for item in data.get("results"):
            movie_details_url = f"{self.movie_details_url}{item.get('id')}"
            yield scrapy.Request(url=movie_details_url, callback=self.get_movie_details)

        if page < total_pages:
            page += 1
            next_page_url = f"{self.movie_changes_url}page={page}"
            yield scrapy.Request(url=next_page_url, callback=self.get_changed_movies)
