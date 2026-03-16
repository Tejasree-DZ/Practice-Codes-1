from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional
import re

class UserCreate(BaseModel):
    mail: EmailStr; name: str; password: str
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8: raise ValueError('Password must be at least 8 characters')
        if not re.search(r'\d', v): raise ValueError('Password must contain at least one digit')
        if not re.search(r'[A-Z]', v): raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v): raise ValueError('Password must contain at least one lowercase letter')
        return v
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or v.isspace(): raise ValueError('Name cannot be blank')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None; password: Optional[str] = None; is_active: Optional[bool] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str; mail: str; name: str; is_active: bool
    last_login: Optional[int]; type_id: Optional[int]
    created_at: int; deleted_at: int

class UserListResponse(BaseModel):
    users: list[UserResponse]; total: int