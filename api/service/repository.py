from abc import ABC
from uuid import uuid4

from service.exceptions import ObjectDoesntExists
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from infrastructure.db.models.base import Base
from infrastructure.main import async_session
from service.exceptions import SomethingWentWrong


class AbstractRepository(ABC):
    def read_model(self):
        raise NotImplementedError()

    def create_model(self):
        raise NotImplementedError()

    def update_model(self):
        raise NotImplementedError()

    def delete_model(self):
        raise NotImplementedError()

    def get_or_404(self):
        raise NotImplementedError()


class CRUDRepository(AbstractRepository):
    def __init__(self):
        self.session = async_session

    async def create_model(self, model: Base, data: dict) -> bool:
        async with self.session() as sess:
            query = insert(model).values(id=uuid4(), **data).returning(model.id)

            try:
                res = await sess.execute(query)

                await sess.commit()

            except IntegrityError:
                raise SomethingWentWrong()

        return res.scalar_one()

    async def read_model(self, model: Base, filter_data: dict):
        async with self.session() as sess:
            query = select(model).filter_by(**filter_data)

            result = await sess.execute(query)

            return result.scalars().all()

    async def update_model(self, model: Base, data, object_id: UUID):
        async with self.session() as sess:
            try:
                query = (
                    update(model)
                    .where(model.id == object_id)
                    .values(**data)
                    .returning(model.id)
                )

                result = await sess.execute(query)

                await sess.commit()

            except IntegrityError:
                raise SomethingWentWrong()

            return result.scalar_one()

    async def delete_model(self, model, object_id):
        async with self.session() as sess:
            query = delete(model).where(model.id == object_id)
            res = await sess.execute(query)

            await sess.commit()

            return res.rowcount

    async def get_owner(self, model: Base, object_id: UUID):
        async with self.session() as sess:
            query = select(model).where(model.id == object_id)
            result = await sess.execute(query)
            if not object:
                raise ObjectDoesntExists(model)

            return result.scalars().one().owner_id
