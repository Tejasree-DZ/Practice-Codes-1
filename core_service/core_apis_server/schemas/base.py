from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TimestampMixin(BaseSchema):
    created_at: int
    deleted_at: int


class PaginatedResponse(BaseSchema):
    total: int