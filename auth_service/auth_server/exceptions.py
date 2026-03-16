# exceptions.py
import enum
from http import HTTPStatus


class Err(enum.Enum):
    OA0002 = ["Method not allowed"]
    OA0003 = ["%s %s not found"]
    OA0005 = ["User %s does not exist"]
    OA0007 = ["This resource requires authorization"]
    OA0010 = ["Token not found"]
    OA0011 = ["Invalid token"]
    OA0012 = ["Forbidden!"]
    OA0017 = ["Role with id %s not assignable to user %s"]
    OA0019 = ["Assignment with id %s not found"]
    OA0020 = ["Invalid type %s"]
    OA0021 = ["Parameter \"%s\" is immutable"]
    OA0022 = ["Unexpected parameters: %s"]
    OA0023 = ["Unauthorized"]
    OA0024 = ["User %s was not found"]
    OA0025 = ["Role %s was not found"]
    OA0028 = ["%s with id %s was not found"]
    OA0031 = ["%s is required"]
    OA0032 = ["%s is not provided"]
    OA0033 = ["%s should be a string"]
    OA0035 = ["Role %s already exists"]
    OA0037 = ["Email or password is invalid"]
    OA0038 = ["User is inactive"]
    OA0039 = ["Email and/or password is not provided"]
    OA0041 = ["Password should be at least 4 characters"]
    OA0042 = ["User %s already exists"]
    OA0043 = ["User with id %s not found"]
    OA0044 = ["Email has invalid format"]
    OA0045 = ["Invalid model type: %s"]
    OA0048 = ["%s should contain %s-%s characters"]
    OA0050 = ["Incorrect request body received"]
    OA0053 = ["Not found"]
    OA0055 = ["%s should be list"]
    OA0056 = ["Type with id %s not found"]
    OA0061 = ["Database error: %s"]
    OA0062 = ["This resource requires an authorization token"]
    OA0063 = ["%s should be true or false"]
    OA0065 = ["%s should not contain only whitespaces"]
    OA0074 = ["Validation error: %s"]


class AuthException(Exception):
    
    http_status: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, error: Err, params: list = None):
        self.error   = error
        self.params  = params or []
        self.message = (
            error.value[0] % tuple(self.params)
            if self.params
            else error.value[0]
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


class NotFoundException(AuthException):
    
    http_status: int = HTTPStatus.NOT_FOUND


class UnauthorizedException(AuthException):
    
    http_status: int = HTTPStatus.UNAUTHORIZED


class ForbiddenException(AuthException):
    
    http_status: int = HTTPStatus.FORBIDDEN


class ConflictException(AuthException):
    
    http_status: int = HTTPStatus.CONFLICT


class WrongArgumentsException(AuthException):
    
    http_status: int = HTTPStatus.BAD_REQUEST


class InvalidTokenException(AuthException):
    
    http_status: int = HTTPStatus.UNAUTHORIZED


class InvalidTreeException(AuthException):
   
    http_status: int = HTTPStatus.BAD_REQUEST