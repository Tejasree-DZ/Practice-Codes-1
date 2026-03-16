from pydantic import BaseModel, ConfigDict
from typing import Optional

class TypeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; name: str; assignable: bool; parent_id: Optional[int]
    created_at: int; deleted_at: int

class TypeListResponse(BaseModel):
    types: list[TypeResponse]; total: int