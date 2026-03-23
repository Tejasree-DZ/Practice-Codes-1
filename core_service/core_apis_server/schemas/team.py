from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class TeamCreate(BaseModel):
    name:        str
    description: Optional[str] = None
    parent_id:   Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or v.isspace():
            raise ValueError('Name cannot be blank')
        if len(v) > 256:
            raise ValueError('Name must be less than 256 characters')
        return v


class TeamUpdate(BaseModel):
    name:        Optional[str] = None
    description: Optional[str] = None


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:              str
    name:            str
    description:     Optional[str] = None
    organization_id: str
    parent_id:       Optional[str] = None
    created_at:      int
    deleted_at:      int


class TeamListResponse(BaseModel):
    teams: list[TeamResponse]
    total: int