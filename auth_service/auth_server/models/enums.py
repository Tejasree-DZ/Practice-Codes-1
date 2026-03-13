from enum import Enum


class RoleEnum(Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class ResourceTypeEnum(Enum):
    organization = "organization"
    team = "team"
