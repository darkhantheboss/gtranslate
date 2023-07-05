from humps import camelize
from pydantic import BaseModel, validator
from sqlalchemy.orm import Query


def to_camel(string: str) -> str:
    """
    Func to create an alias from snake case variables
    """
    return str(camelize(string))


class CamelModel(BaseModel):
    """
    Base model to auto create a camelCase alias.
    Also allows population of Pydantic model via alias
    """

    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        """Config"""

        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True


class SnakeModel(BaseModel):

    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        """Config"""

        orm_mode = True
        allow_population_by_field_name = True
