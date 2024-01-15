from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from infrastructure.db.models.movie import Movie


class MovieFilter(Filter):
    title: Optional[str]

    class Constants(Filter.Constants):
        model = Movie
