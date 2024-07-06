from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from datetime import datetime

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db import Base, Movie, Genre


class ProcessItemPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Transform relative url to absolute
        url_keys = ["backdrop_path", "poster_path"]
        for url_key in url_keys:
            value = adapter.get(url_key)
            if value:
                url = "https://image.tmdb.org/t/p/original/" + value
                adapter[url_key] = url

        # Get list of genres instead of list of dictionaries
        # genres_dict = adapter.get("genres")
        # genres_list = [genre["name"] for genre in genres_dict]
        # adapter["genres"] = genres_list

        # Get the first country in origin country list
        origin_country_list_value = adapter.get("origin_country")
        if origin_country_list_value:
            adapter["origin_country"] = origin_country_list_value[0]

        # Transform release date to Date object
        release_date_string = adapter.get("release_date")
        if release_date_string:
            release_date_value = datetime.strptime(release_date_string, "%Y-%m-%d").date()
            adapter["release_date"] = release_date_value

        # Drop items if they don't contain necessary data
        important_keys = ["genres", "origin_country", "original_title", "title", "release_date", "runtime"]
        for key in important_keys:
            key_value = adapter.get(key)
            if not key_value:
                raise DropItem("Dropping item with insufficient data!")
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

    def process_item(self, item, spider):
        movie = self.session.query(Movie).filter_by(id=item["id"]).first()
        if not movie:
            movie = Movie()
            self.session.add(movie)

        for field, value in item.items():
            if field != "genres":
                setattr(movie, field, value)

        for genre_item in item["genres"]:
            genre = self.session.query(Genre).filter_by(id=genre_item["id"]).first()
            if not genre:
                genre = Genre()
                self.session.add(genre)

            for field, value in genre_item.items():
                setattr(genre, field, value)

            if genre not in movie.genres:
                movie.genres.append(genre)

        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
