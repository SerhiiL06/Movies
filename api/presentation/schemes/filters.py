from fastapi_filter.contrib.sqlalchemy import Filter
from infrastructure.db.models.movie import Movie
from typing import Optional


class MovieFilter(Filter):
    title: Optional[str]

    class Constants(Filter.Constants):
        model = Movie
