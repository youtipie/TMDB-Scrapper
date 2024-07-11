import scrapy


class MediaItem(scrapy.Item):
    id = scrapy.Field()
    backdrop_path = scrapy.Field()
    genres = scrapy.Field()
    origin_country = scrapy.Field()
    original_title = scrapy.Field()
    poster_path = scrapy.Field()
    release_date = scrapy.Field()

    vote_average = scrapy.Field()
    translations = scrapy.Field()


class MovieItem(MediaItem):
    runtime = scrapy.Field()


class TVSeriesItem(MediaItem):
    in_production = scrapy.Field()
    number_of_episodes = scrapy.Field()
    number_of_seasons = scrapy.Field()
    status = scrapy.Field()
    # TODO: Add seasons? Is it worth it?


class TranslationItem(scrapy.Item):
    language = scrapy.Field()
    is_default = scrapy.Field()


class MovieAndSeriesTranslationItem(TranslationItem):
    overview = scrapy.Field()
    title = scrapy.Field()


class GenreItem(TranslationItem):
    id = scrapy.Field()
    name = scrapy.Field()
