from abc import ABCMeta
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel
from sqlalchemy.orm import Session


class BaseRepository(metaclass=ABCMeta):
    async def get_all(
        self, filters: Optional[BaseModel]
    ) -> Tuple[List[BaseModel], int]:
        raise NotImplementedError()

    async def get_by_id(self, obj_id: int) -> BaseModel:
        raise NotImplementedError()

    async def get_by(self, obj_attribute: str, obj_attribute_value: Any) -> BaseModel:
        raise NotImplementedError()

    async def get_like(self, obj_attribute: str, obj_attribute_value: Any) -> BaseModel:
        raise NotImplementedError()

    async def insert(self, new_obj_data: Dict, session: Optional[Session] = None) -> BaseModel:
        raise NotImplementedError()

    async def update(self, obj_id: int, new_obj_data: Dict, session: Optional[Session] = None) -> BaseModel:
        raise NotImplementedError()

    async def remove(self, obj_id: int, session: Optional[Session] = None) -> BaseModel:
        raise NotImplementedError()
