# exceptions.py
from fastapi import HTTPException, status


class ResourceNotFound(HTTPException):
    """Raised when a requested resource does not exist."""
    def __init__(self, resource: str, resource_id: int = None):
        detail = f"{resource} not found"
        if resource_id is not None:
            detail += f" with id {resource_id}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AuthenticationError(HTTPException):
    """Raised when login or authentication fails."""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class AuthorizationError(HTTPException):
    """Raised when a user does not have permission to perform an action."""
    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class ValidationError(HTTPException):
    """Raised when input validation fails beyond Pydantic schemas."""
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)


class ConflictError(HTTPException):
    """Raised when trying to create a resource that already exists."""
    def __init__(self, resource: str, message: str = None):
        detail = message or f"{resource} already exists"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class BadRequestError(HTTPException):
    """Generic 400 error for bad requests."""
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)