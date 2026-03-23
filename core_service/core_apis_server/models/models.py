import uuid

from sqlalchemy import (
    Column, String, Integer, Boolean, TEXT,
    ForeignKey, UniqueConstraint, Table, inspect
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, declared_attr, relationship


def as_dict(obj) -> dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def gen_id() -> str:
    return str(uuid.uuid4())


class PermissionKeys:
    is_creatable = 'is_creatable'
    is_updatable = 'is_updatable'


class ColumnPermissions:
    full        = {PermissionKeys.is_creatable: True,  PermissionKeys.is_updatable: True}
    create_only = {PermissionKeys.is_creatable: True,  PermissionKeys.is_updatable: False}
    update_only = {PermissionKeys.is_creatable: False, PermissionKeys.is_updatable: True}


class _Base:
    __name__: str
    __table__: Table

    def __init__(self, **kwargs):
        init_columns = list(filter(
            lambda x: x.info.get(PermissionKeys.is_creatable) is True,
            self.__table__.c,
        ))
        for col in init_columns:
            setattr(self, col.name, kwargs.get(col.name))
            kwargs.pop(col.name, None)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


Base = declarative_base(cls=_Base)


class BaseModel:
    id         = Column(String(36), primary_key=True, default=gen_id)
    created_at = Column(Integer, nullable=False, default=0)
    deleted_at = Column(Integer, default=0, nullable=False)

    @hybrid_property
    def deleted(self) -> bool:
        return self.deleted_at != 0


class Organization(Base, BaseModel):
    __tablename__ = 'organizations'

    name          = Column(String(256), nullable=False,
                           info=ColumnPermissions.full)
    description   = Column(TEXT, nullable=True,
                           info=ColumnPermissions.full)
    teams_count   = Column(Integer, nullable=False, default=0)
    members_count = Column(Integer, nullable=False, default=0)

    teams = relationship(
        'Team',
        back_populates='organization',
        primaryjoin='and_(Organization.id == Team.organization_id, Team.deleted_at == 0)',
        lazy='dynamic',
    )

    __table_args__ = (
        UniqueConstraint('name', 'deleted_at',
                         name='uq_organization_name_deleted_at'),
    )

    def __init__(self, name=None, description=None):
        self.name        = name
        self.description = description

    def to_schema(self):
        from core_service.core_apis_server.schemas.organization import OrganizationResponse
        return OrganizationResponse.model_validate(self)

    def __repr__(self):
        return f'<Organization {self.name}>'


class Team(Base, BaseModel):
    __tablename__ = 'teams'

    name            = Column(String(256), nullable=False,
                             info=ColumnPermissions.full)
    description     = Column(TEXT, nullable=True,
                             info=ColumnPermissions.full)
    organization_id = Column(String(36), ForeignKey('organizations.id'),
                             nullable=False, info=ColumnPermissions.create_only)
    parent_id       = Column(String(36), ForeignKey('teams.id'),
                             nullable=True, info=ColumnPermissions.create_only)

    organization = relationship('Organization', back_populates='teams')
    parent       = relationship('Team', remote_side='Team.id', backref='sub_teams')
    members      = relationship(
        'Member',
        back_populates='team',
        primaryjoin='and_(Team.id == Member.team_id, Member.deleted_at == 0)',
        lazy='dynamic',
    )

    __table_args__ = (
        UniqueConstraint('name', 'organization_id', 'deleted_at',
                         name='uq_team_name_org_deleted_at'),
    )

    def __init__(self, name=None, description=None,
                 organization_id=None, parent_id=None):
        self.name            = name
        self.description     = description
        self.organization_id = organization_id
        self.parent_id       = parent_id

    def to_schema(self):
        from core_service.core_apis_server.schemas.team import TeamResponse
        return TeamResponse.model_validate(self)

    def __repr__(self):
        return f'<Team {self.name}>'


class Member(Base, BaseModel):
    __tablename__ = 'members'

    team_id      = Column(String(36), ForeignKey('teams.id'),
                          nullable=False, info=ColumnPermissions.create_only)
    auth_user_id = Column(String(36), nullable=False,
                          info=ColumnPermissions.create_only)

    team = relationship('Team', back_populates='members')

    __table_args__ = (
        UniqueConstraint('team_id', 'auth_user_id', 'deleted_at',
                         name='uq_member_team_user_deleted_at'),
    )

    def __init__(self, team_id=None, auth_user_id=None):
        self.team_id      = team_id
        self.auth_user_id = auth_user_id

    def to_schema(self):
        from core_service.core_apis_server.schemas.member import MemberResponse
        return MemberResponse.model_validate(self)

    def __repr__(self):
        return f'<Member team={self.team_id} user={self.auth_user_id}>'