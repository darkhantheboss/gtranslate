from typing import Dict, Tuple, Optional, Union, List

from humps import decamelize
from pydantic import BaseModel


class OffsetParams(BaseModel):
    limit: int = 10
    offset: int = 0
    order_by: Optional[str] = "-created_date"
    search: Optional[str] = ""
    projection: Optional[str] = ""

    @property
    def common_keys(self) -> Tuple:
        return "offset", "limit", "projection"

    @property
    def common_values(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if k in self.common_keys}

    @property
    def values(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if k not in self.common_keys and v}

    @property
    def order_by_query(self) -> str:
        query = ''
        if self.order_by:
            query_direction = 'DESC' if '-' in self.order_by else 'ASC'
            query = f"{decamelize(self.order_by).replace('-', '')} {query_direction}"
        return query

    class Config:
        use_enum_values = True
