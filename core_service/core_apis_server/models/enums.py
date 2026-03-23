import enum


class MemberRole(enum.Enum):
    admin   = 'admin'
    manager = 'manager'
    member  = 'member'