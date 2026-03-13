from pydantic import BaseModel


class AssignmentCreate(BaseModel):

    user_id: int
    role_id: int
    type_id: int
    resource_id: int


class AssignmentResponse(BaseModel):

    id: int
    user_id: int
    role_id: int
    type_id: int
    resource_id: int