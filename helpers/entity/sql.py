from sqlalchemy import Boolean, Column, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeMeta, registry

mapper_registry = registry()


class Base(metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata


class SqlEntity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_date = Column(DateTime, nullable=False, server_default=func.now())
    modified_date = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.__dict__)


def setattrs(_self, **kwargs):
    for k, v in kwargs.items():
        setattr(_self, k, v)


def map_ids(old_ids: list, new_ids: list) -> dict:
    return {
        "to_delete": list(set(old_ids) - set(new_ids)),
        "to_add": list(set(new_ids) - set(old_ids)),
    }
