from typing import Any, List, Optional, Tuple

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import delete, or_, select, update, func, desc
from sqlalchemy.orm import Query, Session, load_only

from helpers.engine.sql import get_sql_session
from helpers.repository.base_repository import BaseRepository


class SQLRepository(BaseRepository):
    def __init__(self, model: Any, factory: Any, schema: BaseModel) -> None:
        self._session = get_sql_session()
        self.model = model
        self.factory = factory
        self.schema = schema

    def __enter__(self) -> "SQLRepository":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._session.remove()

    async def __entity_exists(self, query: Query) -> Optional[Any]:
        async with self._session() as session:
            results = await session.execute(query)
            result = results.one_or_none()
            if result is None:
                return
            (entity,) = result
            return entity

    async def count(self, filters: Any = None) -> int:
        query = select(self.model.id)
        if filters is not None:
            query = query.where(filters)
        async with self._session() as session:
            result = await session.execute(select(func.count()).select_from(query))
            return result.scalar_one()

    async def get(
        self, filters: Any = None, limit: int = None, offset: int = None, sort = None
    ) -> List[BaseModel]:
        query = select(self.model)
        if filters is not None:
            query = query.where(filters)
        if limit is not None and offset is not None:
            query = query.limit(limit).offset(offset)
        async with self._session() as session:
            results = await session.execute(query.order_by(desc(self.model.created_date)))
            results = results.scalars()
            return list(results)

    async def get_all(self, filters: Any = Depends()) -> Tuple[List[BaseModel], int]:
        print("HELO")
        common_values = filters.common_values
        query = (
            select(self.model)
            .where()
            .limit(common_values["limit"])
            .offset(common_values["offset"])
        )
        print(common_values)
        print(filters)
        if common_values.get("projection"):
            projection = common_values["projection"].split(",")
            print(projection)
            query = query.options(
                load_only(
                    *[
                        getattr(self.model, column_name)
                        for column_name in projection
                    ]
                )
            )
        async with self._session() as session:
            results = await session.execute(query.order_by(desc(self.model.created_date)))
            results = results.scalars()
            results = [self.schema.from_orm(result) for result in results]
            return results, len(results)

    async def get_all_without_filter(self) -> List[BaseModel]:

        query = select(self.model).where()

        async with self._session() as session:
            results = await session.execute(query)
            results = results.scalars()
            return [self.schema.from_orm(res) for res in results]

    async def get_by_id(self, obj_id: int) -> Any:
        query = select(self.model).where(self.model.id == obj_id)
        entity = await self.__entity_exists(query)
        return self.schema.from_orm(entity)

    async def get_by(self, obj_attribute: str, obj_attribute_value: Any) -> Any:
        obj_attribute = getattr(self.model, obj_attribute)
        query = select(self.model).where(obj_attribute == obj_attribute_value)
        entity = await self.__entity_exists(query)
        result = self.schema.from_orm(entity) if entity else None
        return result

    async def get_like(self, obj_attribute: str, obj_attribute_value: Any) -> Any:
        obj_attribute = getattr(self.model, obj_attribute)
        query = select(self.model).where(obj_attribute.like(f"{obj_attribute_value}%"))
        entity = await self.__entity_exists(query)
        result = self.schema.from_orm(entity) if entity else None
        return result

    async def get_many_by_text_field(
        self, obj_attribute: str, obj_attribute_value: str
    ) -> Any:
        obj_attribute = getattr(self.model, obj_attribute)

        query = select(self.model).where(
            or_(
                obj_attribute == obj_attribute_value,
                obj_attribute.like(f"{obj_attribute_value.capitalize()}%"),
                obj_attribute.like(f"{obj_attribute_value.lower()}%"),
            )
        )

        async with self._session() as session:
            results = await session.execute(query)
            results = results.scalars()
            return [self.schema.from_orm(res) for res in results]

    async def get_many_by_field(
        self, obj_attribute: str, obj_attribute_value: Any
    ) -> Any:
        obj_attribute = getattr(self.model, obj_attribute)

        query = select(self.model).where(obj_attribute == obj_attribute_value)

        async with self._session() as session:
            results = await session.execute(query)
            results = results.scalars()
            return [self.schema.from_orm(res) for res in results]

    async def __get_session(self, session: Optional[Session]):
        if session is None:
            async with self._session() as _session:
                return _session
        return session

    @staticmethod
    async def __complete_session(
            received_session: Optional[Session],
            current_session: Session,
            entity=None,
    ):
        if received_session is None:
            await current_session.commit()
        else:
            await current_session.flush()

        if entity is not None:
            await current_session.refresh(entity)

        if received_session is None:
            await current_session.close()

    async def insert(self, new_obj_data: Any, session=None) -> Any:
        _session = await self.__get_session(session)
        _session.add(new_obj_data)
        await self.__complete_session(received_session=session, current_session=_session, entity=new_obj_data)
        return self.schema.from_orm(new_obj_data)

    async def upsert(
            self,
            obj_attribute: str,
            obj_attribute_value: Any,
            new_obj_data: Any,
            schemas: Tuple[Any, Any],
            session=None
    ) -> Any:
        obj_attribute = getattr(self.model, obj_attribute)
        query = select(self.model).where(obj_attribute == obj_attribute_value)
        entity = await self.__entity_exists(query)
        _session = await self.__get_session(session)

        if entity:
            query = (
                update(self.model)
                .where(obj_attribute == obj_attribute_value)
                .values(schemas[1](**new_obj_data).dict(exclude_unset=True))
            )
            _session.add(entity)
            await _session.execute(query)
            await self.__complete_session(received_session=session, current_session=_session, entity=entity)
            new_object = self.schema.from_orm(entity)
        else:
            new_obj = self.model(**schemas[0](**new_obj_data).dict())
            _session.add(new_obj)
            await self.__complete_session(received_session=session, current_session=_session, entity=new_obj)
            new_object = self.schema.from_orm(new_obj)

        return new_object

    async def update(self, obj_id: int, new_obj_data: Any, session=None) -> Any:
        query = select(self.model).where(self.model.id == obj_id)
        entity = await self.__entity_exists(query)
        query = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(new_obj_data.dict())
        )
        _session = await self.__get_session(session)
        _session.add(entity)
        await _session.execute(query)
        await self.__complete_session(received_session=session, current_session=_session, entity=entity)
        return self.schema.from_orm(entity)

    async def update_many(self, obj_ids: tuple[int], new_obj_data: dict) -> Any:
        query = (
            update(self.model).where(self.model.id.in_(obj_ids)).values(new_obj_data)
        )
        async with self._session() as session:
            await session.execute(query)
            await session.commit()

    async def remove_by_field(
        self, obj_attribute: str, obj_attribute_value: Any
    ) -> Any:
        obj_attribute = getattr(self.model, obj_attribute)

        query = select(self.model).where(obj_attribute == obj_attribute_value)

        query = delete(self.model).where(obj_attribute == obj_attribute_value)
        async with self._session() as session:
            await session.execute(query)
            await session.commit()
            await self.__complete_session(received_session=session, current_session=session)

    async def remove(self, obj_id: int, session=None) -> Any:
        pass

    async def remove_by_field_m2m(
            self,
            left_attribute_name: str,
            left_attribute_value: Any,
            right_attribute_name: str,
            right_attribute_value: Any,
            session=None
    ) -> None:
        left_attribute = getattr(self.model, left_attribute_name)
        right_attribute = getattr(self.model, right_attribute_name)
        select_query = (
            select(self.model)
            .where(left_attribute == left_attribute_value)
            .where(right_attribute == right_attribute_value)
        )

        await self.__entity_exists(select_query)

        delete_query = (
            delete(self.model)
            .where(left_attribute == left_attribute_value)
            .where(right_attribute == right_attribute_value)
        )
        _session = await self.__get_session(session)
        await _session.execute(delete_query)
        await self.__complete_session(received_session=session, current_session=_session)

    async def get_all_by_ids(self, ids: List[int]) -> List[BaseModel]:
        query = select(self.model).where(self.model.id.in_(ids))

        async with self._session() as session:
            results = await session.execute(query)
            results = results.scalars()
            return [self.schema.from_orm(res) for res in results]

    async def get_cursor(self, filters):
        query = (
            select(self.model)
            .where(*filters)
        )

        async with self._session() as session:
            results = await session.execute(query)
            return results.scalars()
