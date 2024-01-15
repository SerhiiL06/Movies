from datetime import date
from typing import Annotated
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column

idpk = Annotated[UUID, mapped_column(unique=True, primary_key=True)]
create = Annotated[date, mapped_column(default=func.now())]


class Base(DeclarativeBase):
    pass
