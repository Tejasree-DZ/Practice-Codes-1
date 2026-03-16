import enum

class RoleName(enum.Enum):
    admin   = 'admin'
    manager = 'manager'
    user    = 'user'

class TypeName(enum.Enum):
    organization = 'organization'
    team         = 'team'

class TokenType(enum.Enum):
    ACCESS  = 'access'
    REFRESH = 'refresh'