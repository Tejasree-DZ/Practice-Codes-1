from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:          int
    name:        str
    description: Optional[str] = None
    type_id:     Optional[int] = None
    is_active:   bool
    shared:      bool
    created_at:  int
    deleted_at:  int


class RoleListResponse(BaseModel):
    roles: list[RoleResponse]
    total: int