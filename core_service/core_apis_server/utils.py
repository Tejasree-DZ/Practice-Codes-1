import hashlib
import re
from datetime import datetime, timezone

from jose import JWTError, jwt
from sqlalchemy import inspect

from core_service.core_apis_server.settings import settings
from core_service.core_apis_server.exceptions import (
    Err, WrongArgumentsException, InvalidTokenException
)


def as_dict(obj) -> dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_current_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def is_email_format(check_str: str) -> bool:
    regex = (r"^[a-z0-9!#$%&\'*+/=?`{|}~\^\-\+_()]+"
             r"(\.[a-z0-9!#$%&\'*+/=?`{|}~\^\-\+_()]+)*"
             r"@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,18})$")
    return bool(re.match(regex, str(check_str).lower()))


def is_uuid(check_str: str) -> bool:
    pattern = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    return bool(re.match(pattern, str(check_str).lower()))


def check_string_attribute(name: str, value, min_length=1, max_length=255):
    if value is None:
        raise WrongArgumentsException(Err.OC0021, [name])
    if not isinstance(value, str):
        raise WrongArgumentsException(Err.OC0023, [name])
    if not min_length <= len(value) <= max_length:
        raise WrongArgumentsException(Err.OC0024, [name, min_length, max_length])
    if value.isspace():
        raise WrongArgumentsException(Err.OC0022, [name])


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise InvalidTokenException(Err.OC0008)
        return user_id
    except JWTError:
        raise InvalidTokenException(Err.OC0008)