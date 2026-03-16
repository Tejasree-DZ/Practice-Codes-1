from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssignmentCreate(BaseModel):
    user_id: str; role_id: int; type_id: int; resource_id: Optional[str] = None

class AssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str; user_id: str; role_id: int; type_id: int
    resource_id: Optional[str]; created_at: int; deleted_at: int

class AssignmentListResponse(BaseModel):
    assignments: list[AssignmentResponse]; total: int