from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import func
from typing import Annotated
from uuid import UUID
from datetime import date

idpk = Annotated[UUID, mapped_column(unique=True, primary_key=True)]
create = Annotated[date, mapped_column(default=func.now())]


class Base(DeclarativeBase):
    pass
