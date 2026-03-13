from pydantic import BaseModel


class TypeCreate(BaseModel):

    name: str
    description: str | None = None


class TypeResponse(BaseModel):

    id: int
    name: str
    description: str | None