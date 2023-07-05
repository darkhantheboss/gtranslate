from sqlalchemy import Column, String, JSON

from helpers.entity.sql import SqlEntity


class Translate(SqlEntity):
    __tablename__ = "translations"

    word = Column(String(256), nullable=False)
    info = Column(JSON)
