import scrapy


class MovieItem(scrapy.Item):
    id = scrapy.Field()
    backdrop_path = scrapy.Field()
    genres = scrapy.Field()
    origin_country = scrapy.Field()
    original_title = scrapy.Field()
    overview = scrapy.Field()
    poster_path = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()
    title = scrapy.Field()
    vote_average = scrapy.Field()

    def __repr__(self):
        return f"<{self['title']}>"
