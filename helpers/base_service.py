from typing import Any, Dict, List

from pydantic import BaseModel

from helpers.repository.sql_repository import SQLRepository


class BaseService:
    repository: SQLRepository

    async def count(self, filters: Any = None) -> int:
        if filters is not None:
            return await self.repository.count(filters)
        return await self.repository.count()

    async def get(
        self, filters: Any = None, limit: int = None, offset: int = None, sort = None
    ) -> Any:
        return await self.repository.get(filters, limit, offset, sort)

    async def get_all(self, filters: Any) -> Dict:
        results = await self.repository.get_all(filters)
        response = dict(results=results)

        if (
            not isinstance(filters, dict)
            and filters.common_values.get("projection") is not None
        ):
            response["projection"] = filters.common_values["projection"]
        return response

    async def get_by(self, obj_attribute: str, obj_attribute_value: Any) -> Any:
        result = await self.repository.get_by(obj_attribute, obj_attribute_value)
        return result

    async def get_like(self, obj_attribute: str, obj_attribute_value: Any) -> Any:
        result = await self.repository.get_like(obj_attribute, obj_attribute_value)
        return result

    async def get_by_id(self, obj_id: int) -> Any:
        result = await self.repository.get_by_id(obj_id)
        return result

    async def delete_by_id(self, obj_id: int) -> Any:
        result = await self.repository.delete_by_id(obj_id)
        return result

    async def get_all_by_ids(self, ids: List) -> List[Any]:
        return await self.repository.get_all_by_ids(ids)

    async def get_many_by_field(self, obj_attribute: str, obj_attribute_value: Any):
        return await self.repository.get_many_by_field(
            obj_attribute, obj_attribute_value
        )

    async def get_m2m_model_ids(
        self, field_name, field_value, model_field_name
    ) -> List[int]:
        model_data = await self.get_many_by_field(field_name, field_value)
        model_ids = []
        if model_data:
            model_ids = [getattr(md, model_field_name) for md in model_data]
        return model_ids

    async def create(self, obj_data: BaseModel, session=None) -> Any:
        new_obj = self.repository.model(**obj_data.dict())
        result: Any = await self.repository.insert(new_obj, session)
        return result

    async def create_many(self, objs_data: List[BaseModel]) -> Any:
        return await self.repository.bulk_insert(objs_data)

    async def update(self, obj_id: int, obj_data: BaseModel, session=None) -> Any:
        result: Any = await self.repository.update(
            obj_id=obj_id,
            new_obj_data=obj_data,
            session=session)
        return result

    async def update_many(self, obj_ids: tuple[int], new_obj_data: dict) -> Any:
        return await self.repository.update_many(obj_ids, new_obj_data)

    async def remove(self, obj_id: int, session=None) -> None:
        await self.repository.remove(obj_id, session)

    async def remove_by_field(self, obj_attribute: str, obj_attribute_value: Any):
        return await self.repository.remove_by_field(obj_attribute, obj_attribute_value)

    async def remove_m2m_model(
            self,
            left_filed_name,
            left_filed_value,
            right_filed_name,
            right_filed_value,
            session=None
    ) -> None:
        for id_to_remove in right_filed_value:
            await self.repository.remove_by_field_m2m(
                left_filed_name,
                left_filed_value,
                right_filed_name,
                id_to_remove,
                session
            )

    async def append_m2m_model(
        self, field_name, schema, ids_to_append, key, val, session=None
    ) -> None:
        for id_to_append in ids_to_append:
            await self.create(schema(**{key: val}, **{field_name: id_to_append}), session)

    async def get_schema(self, filters: Any, obj_data: Any) -> Dict:
        resp = dict(filters=dict(), projections=dict())
        resp["basicFilters"] = filters.schema()["properties"]
        obj_data_fields = obj_data.__fields__
        resp["filters"] = {}
        for i, j in obj_data_fields.items():
            resp["filters"][i] = {
                repr(v) if a is None else a: v
                for a, v in obj_data_fields[i].__repr_args__()
            }
            resp["projections"][i] = (
                {m: {} for m in i.__fields__}
                if isinstance(obj_data_fields[i], BaseModel)
                else {}
            )
        return resp

    def get_cursor(self, filters):
        return self.repository.get_cursor(filters)

