from sqlalchemy import Column, Integer, String, Float, Text, Date, Table, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

genre_movie_association = Table(
    "genre_movie_association",
    Base.metadata,
    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True)
)

genre_series_association = Table(
    "genre_series_association",
    Base.metadata,
    Column("series_id", ForeignKey("series.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True)
)


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    backdrop_path = Column(String)
    genres = relationship("Genre", secondary=genre_movie_association, back_populates="movies")
    origin_country = Column(String, nullable=False)
    original_title = Column(String, nullable=False)
    poster_path = Column(String)
    release_date = Column(Date, nullable=False)
    runtime = Column(Integer, nullable=False)
    vote_average = Column(Float, nullable=False)
    translations = relationship("MovieTranslations", back_populates="movie")


class MediaTranslations(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)

    overview = Column(Text)
    title = Column(String, nullable=False)


class MovieTranslations(MediaTranslations):
    __tablename__ = "movie_translations"

    movie_id = Column(ForeignKey("movie.id"), nullable=False)
    movie = relationship("Movie", back_populates="translations")


class SeriesTranslations(MediaTranslations):
    __tablename__ = "series_translations"

    series_id = Column(ForeignKey("series.id"), nullable=False)
    series = relationship("Series", back_populates="translations")


class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True)
    backdrop_path = Column(String)
    genres = relationship("Genre", secondary=genre_series_association, back_populates="series")
    origin_country = Column(String, nullable=False)
    original_title = Column(String, nullable=False)
    poster_path = Column(String)
    release_date = Column(Date, nullable=False)
    in_production = Column(Boolean, nullable=False)
    number_of_episodes = Column(Integer, nullable=False)
    number_of_seasons = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    vote_average = Column(Float, nullable=False)
    translations = relationship("SeriesTranslations", back_populates="series")


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    translations = relationship("GenreTranslations", back_populates="genre")
    movies = relationship("Movie", secondary=genre_movie_association, back_populates="genres")
    series = relationship("Series", secondary=genre_series_association, back_populates="genres")


class GenreTranslations(Base):
    __tablename__ = "genre_translations"
    id = Column(Integer, primary_key=True)
    genre_id = Column(ForeignKey("genre.id"), nullable=False)
    genre = relationship("Genre", back_populates="translations")

    language = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)

    name = Column(String, nullable=False)
