from datetime import datetime
from pydantic import BaseModel


class BaseSchema(BaseModel):

    id: int | None = None
    created_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True