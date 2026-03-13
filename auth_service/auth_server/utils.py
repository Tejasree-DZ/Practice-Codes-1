import enum
import hashlib
import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt
from sqlalchemy import inspect

from auth_service.auth_server.settings import settings


MAX_32_INT = 2 ** 31 - 1



def as_dict(obj) -> dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, enum.Enum):
            return obj.value
        if isinstance(obj, bytes):
            return obj.decode()
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def is_email_format(check_str: str) -> bool:
    regex = (r"^[a-z0-9!#$%&\'*+/=?`{|}~\^\-\+_()]+"
             r"(\.[a-z0-9!#$%&\'*+/=?`{|}~\^\-\+_()]+)*"
             r"@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,18})$")
    return bool(re.match(regex, str(check_str).lower()))


def is_uuid(check_str: str) -> bool:
    pattern = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    return bool(re.match(pattern, str(check_str).lower()))


def strtobool(val: str) -> bool:
    val = val.lower()
    if val not in ['true', 'false']:
        raise ValueError('Should be false or true')
    return val == 'true'


def unique_list(list_to_filter: list) -> list:
    return list(set(list_to_filter))


def get_input(keys: list, **inputs) -> dict:
    return dict(filter(lambda x: x[1] is not None,
                       {key: inputs.get(key) for key in keys}.items()))


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256(
        password.encode('utf-8') + salt.encode('utf-8')
    ).hexdigest()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    return hash_password(password, salt) == hashed


def get_digest(val: str) -> str:
    return hashlib.md5(val.encode('utf-8')).hexdigest()


def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra: dict[str, Any] | None = None,
) -> str:
    from auth_service.auth_server.models.enums import TokenType
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET_KEY,
                      algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: str) -> str:
    from auth_service.auth_server.models.enums import TokenType
    return _create_token(
        subject=user_id,
        token_type=TokenType.ACCESS.value,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: str) -> str:
    from auth_service.auth_server.models.enums import TokenType
    return _create_token(
        subject=user_id,
        token_type=TokenType.REFRESH.value,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str, expected_type) -> str:
    from auth_service.auth_server.exceptions import InvalidTokenException
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != expected_type.value:
            raise InvalidTokenException(
                f"Expected {expected_type.value} token.")
        user_id: str = payload.get("sub")
        if not user_id:
            raise InvalidTokenException()
        return user_id
    except JWTError as exc:
        raise InvalidTokenException(str(exc))


def check_string_attribute(name: str, value, min_length=1, max_length=255):
    from auth_service.auth_server.exceptions import WrongArgumentsException
    if value is None:
        raise WrongArgumentsException(f"{name} is required.")
    if not isinstance(value, str):
        raise WrongArgumentsException(f"{name} must be a string.")
    if not min_length <= len(value) <= max_length:
        raise WrongArgumentsException(
            f"{name} must be between {min_length} and {max_length} characters.")
    if value.isspace():
        raise WrongArgumentsException(f"{name} cannot be blank.")


def check_bool_attribute(name: str, value):
    from auth_service.auth_server.exceptions import WrongArgumentsException
    if not isinstance(value, bool):
        raise WrongArgumentsException(f"{name} must be a boolean.")


def check_list_attribute(name: str, value, required=True):
    from auth_service.auth_server.exceptions import WrongArgumentsException
    if value is None:
        if not required:
            return
        raise WrongArgumentsException(f"{name} is required.")
    if not isinstance(value, list):
        raise WrongArgumentsException(f"{name} must be a list.")
    

