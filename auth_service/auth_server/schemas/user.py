from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    email: EmailStr
    name: str
    password: str


class UserUpdate(BaseModel):

    name: str | None = None
    password: str | None = None


class UserResponse(BaseModel):

    id: int
    email: EmailStr
    name: str

class UserUpdate(BaseModel):
    email: str
    password: str
    name: str