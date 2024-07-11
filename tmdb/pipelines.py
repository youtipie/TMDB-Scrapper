from datetime import datetime

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, CloseSpider
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db import Base, Movie, Genre, MovieTranslations, GenreTranslations, Series, SeriesTranslations
from .items import MovieItem, TVSeriesItem


class MediaItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Transform relative url to absolute
        url_keys = ["backdrop_path", "poster_path"]
        for url_key in url_keys:
            value = adapter.get(url_key)
            if value:
                url = "https://image.tmdb.org/t/p/original/" + value
                adapter[url_key] = url

        # Get the first country in origin country list
        origin_country_list_value = adapter.get("origin_country")
        if origin_country_list_value:
            adapter["origin_country"] = origin_country_list_value[0]

        # Transform release date to Date object
        release_date_string = adapter.get("release_date")
        if release_date_string and isinstance(release_date_string, str):
            release_date_value = datetime.strptime(release_date_string, "%Y-%m-%d").date()
            adapter["release_date"] = release_date_value

        # Set overview value to None if it is empty string
        for translation in adapter.get("translations"):
            translation_overview_value = translation.get("overview")
            translation["overview"] = None if translation_overview_value == "" else translation_overview_value

        # Drop items if they don't contain necessary data
        important_keys = ["genres", "origin_country", "original_title", "release_date"]

        if isinstance(item, MovieItem):
            important_keys.append("runtime")
        elif isinstance(item, TVSeriesItem):
            important_keys.extend(["number_of_episodes", "number_of_seasons"])

        for key in important_keys:
            key_value = adapter.get(key)
            if not key_value:
                raise DropItem("Dropping item with insufficient data!")
        return item


class GenreItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        name_value = adapter.get("name")
        adapter["name"] = name_value.title()

        return item


class SaveToDB:
    def __init__(self):
        db_uri = get_project_settings().get("DATABASE_URI")
        engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        self.session = Session()
        # self.session.query(Movie).delete()
        # self.session.query(Genre).delete()

    def close_spider(self, spider):
        self.session.close()


class SaveMediaPipeline(SaveToDB):

    def process_item(self, item, spider):
        if isinstance(item, MovieItem):
            media_class = Movie
            translations_class = MovieTranslations
        elif isinstance(item, TVSeriesItem):
            media_class = Series
            translations_class = SeriesTranslations
        else:
            return item

        media = self.session.query(media_class).filter_by(id=item["id"]).first()
        if not media:
            media = media_class()
            self.session.add(media)

        for field, value in item.items():
            if field not in ["genres", "translations"]:
                setattr(media, field, value)

        for translation in media.translations:
            self.session.delete(translation)

        for translation in item["translations"]:
            media_translation = translations_class(**translation)
            media.translations.append(media_translation)
            self.session.add(media_translation)

        for genre_item in item["genres"]:
            genre = self.session.query(Genre).filter_by(id=genre_item["id"]).first()
            if not genre:
                raise CloseSpider("Cannot find corresponding genre for a movie. Please run CategorySpider first!")

            if genre not in media.genres:
                media.genres.append(genre)

        self.session.commit()
        return item


class SaveGenresPipeline(SaveToDB):
    def process_item(self, item, spider):
        genre = self.session.query(Genre).filter_by(id=item["id"]).first()
        if not genre:
            genre = Genre(id=item["id"])
            self.session.add(genre)

        genre_translation = (self.session.query(GenreTranslations)
                             .filter_by(genre_id=genre.id, language=item["language"]).first())
        if not genre_translation:
            genre_translation = GenreTranslations()
            genre_translation.genre = genre
            self.session.add(genre_translation)

        for field, value in item.items():
            if field not in ["id"]:
                setattr(genre_translation, field, value)

        # if genre_translation not in genre.translations:
        #     genre_translation.append(genre_translation)

        self.session.commit()
        return item
