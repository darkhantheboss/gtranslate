import datetime

from pydantic import BaseModel


class CommonModel(BaseModel):
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()
