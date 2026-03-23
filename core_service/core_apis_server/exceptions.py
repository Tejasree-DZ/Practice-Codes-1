import enum
from http import HTTPStatus


class Err(enum.Enum):
    OC0001 = ["Wrong arguments: %s"]
    OC0002 = ["Method not allowed"]
    OC0003 = ["%s %s not found"]
    OC0004 = ["Not found"]
    OC0005 = ["Forbidden"]
    OC0006 = ["Unauthorized"]
    OC0007 = ["%s already exists"]
    OC0008 = ["Invalid token"]
    OC0009 = ["This resource requires authorization"]
    OC0010 = ["Database error: %s"]
    OC0011 = ["Organization with id %s not found"]
    OC0012 = ["Team with id %s not found"]
    OC0013 = ["Member with id %s not found"]
    OC0014 = ["%s with id %s was not found"]
    OC0015 = ["Organization %s already exists"]
    OC0016 = ["Team %s already exists"]
    OC0017 = ["Member already exists in team"]
    OC0018 = ["Token validator not found"]
    OC0019 = ["Config not found"]
    OC0020 = ["Validation error: %s"]
    OC0021 = ["%s is required"]
    OC0022 = ["%s should not contain only whitespaces"]
    OC0023 = ["%s should be a string"]
    OC0024 = ["%s should contain %s-%s characters"]


class CoreException(Exception):
    http_status: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, error: Err, params: list = None):
        self.error      = error
        self.params     = params or []
        self.message    = (
            error.value[0] % tuple(self.params)
            if self.params else error.value[0]
        )
        self.error_code = error.name
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "message":    self.message,
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.error_code}: {self.message})"

    def __str__(self) -> str:
        return self.message


class NotFoundException(CoreException):
    http_status: int = HTTPStatus.NOT_FOUND


class UnauthorizedException(CoreException):
    http_status: int = HTTPStatus.UNAUTHORIZED


class ForbiddenException(CoreException):
    http_status: int = HTTPStatus.FORBIDDEN


class ConflictException(CoreException):
    http_status: int = HTTPStatus.CONFLICT


class WrongArgumentsException(CoreException):
    http_status: int = HTTPStatus.BAD_REQUEST


class InvalidTokenException(CoreException):
    http_status: int = HTTPStatus.UNAUTHORIZED


class FailedDependency(CoreException):
    http_status: int = HTTPStatus.FAILED_DEPENDENCY