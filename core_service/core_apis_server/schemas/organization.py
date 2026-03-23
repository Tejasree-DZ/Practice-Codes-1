from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class OrganizationCreate(BaseModel):
    name:        str
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or v.isspace():
            raise ValueError('Name cannot be blank')
        if len(v) > 256:
            raise ValueError('Name must be less than 256 characters')
        return v


class OrganizationUpdate(BaseModel):
    name:        Optional[str] = None
    description: Optional[str] = None


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:            str
    name:          str
    description:   Optional[str] = None
    teams_count:   int
    members_count: int
    created_at:    int
    deleted_at:    int


class OrganizationListResponse(BaseModel):
    organizations: list[OrganizationResponse]
    total:         int