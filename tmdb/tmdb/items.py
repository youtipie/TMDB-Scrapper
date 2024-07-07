import scrapy


class MovieItem(scrapy.Item):
    id = scrapy.Field()
    backdrop_path = scrapy.Field()
    genres = scrapy.Field()
    origin_country = scrapy.Field()
    original_title = scrapy.Field()
    poster_path = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()
    vote_average = scrapy.Field()

    translations = scrapy.Field()


class TranslationItem(scrapy.Item):
    language = scrapy.Field()
    is_default = scrapy.Field()


class MovieTranslationItem(TranslationItem):
    overview = scrapy.Field()
    title = scrapy.Field()


class GenreItem(TranslationItem):
    id = scrapy.Field()
    name = scrapy.Field()
