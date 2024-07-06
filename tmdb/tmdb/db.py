from sqlalchemy import Column, Integer, String, Float, Text, Date, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

genre_movie_association = Table(
    "genre_movie_association",
    Base.metadata,
    Column("movie_id", ForeignKey("movie.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True)
)


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    backdrop_path = Column(String)
    genres = relationship("Genre", secondary=genre_movie_association, back_populates="movies")
    origin_country = Column(String, nullable=False)
    original_title = Column(String, nullable=False)
    overview = Column(Text)
    poster_path = Column(String)
    release_date = Column(Date, nullable=False)
    runtime = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    vote_average = Column(Float, nullable=False)


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    movies = relationship("Movie", secondary=genre_movie_association, back_populates="genres")
