import hashlib
import re
from datetime import datetime, timezone, timedelta
from typing import Any

from jose import JWTError, jwt
from sqlalchemy import inspect

from auth_service.auth_server.settings import settings
from auth_service.auth_server.exceptions import (
    Err, WrongArgumentsException, InvalidTokenException
)


def as_dict(obj) -> dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def get_current_timestamp() -> int:
    return int(datetime.now(timezone.utc).timestamp())


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256(
        password.encode('utf-8') + salt.encode('utf-8')
    ).hexdigest()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    return hash_password(password, salt) == hashed


def get_digest(val: str) -> str:
    return hashlib.md5(val.encode('utf-8')).hexdigest()


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
        raise WrongArgumentsException(Err.OA0032, [name])
    if not isinstance(value, str):
        raise WrongArgumentsException(Err.OA0033, [name])
    if not min_length <= len(value) <= max_length:
        raise WrongArgumentsException(Err.OA0048, [name, min_length, max_length])
    if value.isspace():
        raise WrongArgumentsException(Err.OA0065, [name])


def _create_token(subject: str, token_type: str,
                  expires_delta: timedelta,
                  extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub":  subject,
        "type": token_type,
        "iat":  now,
        "exp":  now + expires_delta,
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
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != expected_type.value:
            raise InvalidTokenException(Err.OA0011)
        user_id: str = payload.get("sub")
        if not user_id:
            raise InvalidTokenException(Err.OA0011)
        return user_id
    except JWTError:
        raise InvalidTokenException(Err.OA0011)