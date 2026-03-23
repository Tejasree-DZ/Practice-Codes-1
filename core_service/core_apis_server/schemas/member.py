from pydantic import BaseModel, ConfigDict
from typing import Optional


class MemberCreate(BaseModel):
    auth_user_id: str


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:           str
    team_id:      str
    auth_user_id: str
    created_at:   int
    deleted_at:   int


class MemberListResponse(BaseModel):
    members: list[MemberResponse]
    total:   int