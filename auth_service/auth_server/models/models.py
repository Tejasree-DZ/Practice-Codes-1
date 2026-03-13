
import enum
import json
import uuid
import string
import random


from sqlalchemy import (
    Column, String, Integer, Boolean, TEXT,
    ForeignKey, UniqueConstraint, Table, inspect
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, declared_attr, relationship, backref


def as_dict(obj) -> dict:
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class ModelEncoder(json.JSONEncoder):
     def default(self, obj):
        if type(obj).__mro__[1] is enum.Enum:
            return obj.value
        if type(obj) is bytes:
            return obj.decode()
        if type(obj) is set:
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def gen_id() -> str:
    return str(uuid.uuid4())


def gen_salt() -> str:
    return ''.join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(8)
    )

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

    def to_dict(self) -> dict:
        return as_dict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), cls=ModelEncoder)


Base = declarative_base(cls=_Base)


class BaseModel:
    id = Column(String(36), primary_key=True, default=gen_id)
    created_at = Column(Integer, nullable=False)
    deleted_at = Column(Integer, default=0, nullable=False)

    @hybrid_property
    def deleted(self) -> bool:
        return self.deleted_at != 0

    def to_dict(self) -> dict:
        return as_dict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), cls=ModelEncoder)


class Type(Base, BaseModel):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey('type.id'), nullable=True)
    name = Column(String(64), nullable=False, unique=True,
                  info=ColumnPermissions.create_only)
    assignable = Column(Boolean, nullable=False, default=True,
                        info=ColumnPermissions.full)

    children = relationship(
        'Type',
        cascade='all',
        backref=backref('parent', remote_side='Type.id'),
        collection_class=list,
    )

    @hybrid_property
    def child_tree(self) -> list:
        all_ = []

        def get_children(node, li):
            if node:
                items = node.children
                if len(items) == 1:
                    li.append(items[0])
                    get_children(items[0], li)
                elif len(items) > 1:
                    raise Exception("Invalid tree format")
        get_children(self, all_)
        return sorted(all_, key=lambda x: x.id)

    @hybrid_property
    def parent_tree(self) -> list:
        all_ = []

        def get_parents(node, li):
            if node:
                element = node.parent
                if element:
                    li.append(element)
                    get_parents(element, li)
        get_parents(self, all_)
        return sorted(all_, key=lambda x: x.id, reverse=True)

    def __init__(self, id_=None, name=None, parent=None, assignable=True):
        self.id = id_
        self.name = name
        self.parent = parent
        self.assignable = assignable

    def __repr__(self) -> str:
        return f"Type(name={self.name}, id={self.id}, parent_id={self.parent_id})"


class User(Base, BaseModel):
    __tablename__ = 'user'

    mail = Column(String(256), nullable=False,
                  info=ColumnPermissions.create_only)
    name = Column(String(256), nullable=False,
                  info=ColumnPermissions.full)
    password = Column(String(64), nullable=False,
                      info=ColumnPermissions.full)
    salt = Column(String(20), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True,
                       info=ColumnPermissions.full)
    last_login = Column(Integer, nullable=True, default=None,
                        info=ColumnPermissions.update_only)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=True,
                     info=ColumnPermissions.create_only)

    type = relationship('Type', backref='users')
    assignments = relationship(
        'Assignment',
        back_populates='user',
        primaryjoin='and_(User.id == Assignment.user_id, Assignment.deleted_at == 0)',
        lazy='dynamic',
    )

    def __init__(self, mail=None, name=None, password=None, salt=None,
                 type_=None, type_id=None, is_active=True, last_login=None):
        if type_:
            self.type = type_
        if type_id is not None:
            self.type_id = type_id
        self.mail = mail
        self.name = name
        self.password = password
        self.salt = salt if salt else gen_salt()
        self.is_active = is_active
        self.last_login = last_login

    def to_dict(self) -> dict:
        user_dict = as_dict(self)
        return {k: v for k, v in user_dict.items()
                if k not in ('password', 'salt')}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), cls=ModelEncoder)

    def __repr__(self) -> str:
        return f'<User {self.mail}>'


class Role(Base, BaseModel):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False,
                  info=ColumnPermissions.full)
    description = Column(TEXT, nullable=True,
                         info=ColumnPermissions.full)
    type_id = Column(Integer, ForeignKey('type.id'), nullable=True,
                     info=ColumnPermissions.create_only)
    is_active = Column(Boolean, nullable=False, default=True,
                       info=ColumnPermissions.full)
    shared = Column(Boolean, nullable=False, default=False,
                    info=ColumnPermissions.full)

    type = relationship('Type', backref='roles')
    assignments = relationship(
        'Assignment',
        back_populates='role',
        primaryjoin='and_(Role.id == Assignment.role_id, Assignment.deleted_at == 0)',
        lazy='dynamic',
    )

    def __init__(self, name=None, description=None, type_=None, type_id=None,
                 is_active=True, shared=False):
        if type_:
            self.type = type_
        if type_id is not None:
            self.type_id = type_id
        self.name = name
        self.description = description
        self.is_active = is_active
        self.shared = shared

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class Assignment(Base, BaseModel):
    __tablename__ = 'assignment'

    type_id = Column(Integer, ForeignKey('type.id'), nullable=False,
                     info=ColumnPermissions.create_only)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False,
                     info=ColumnPermissions.create_only)
    user_id = Column(String(36), ForeignKey('user.id'), nullable=False,
                     info=ColumnPermissions.create_only)
    resource_id = Column(String(36), nullable=True, index=True,
                         info=ColumnPermissions.create_only)

    user = relationship('User', back_populates='assignments')
    role = relationship('Role', back_populates='assignments')
    type = relationship('Type', backref='assignments')

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'resource_id', 'role_id', 'type_id', 'deleted_at',
            name='uq_assignment_user_role_resource_active',
        ),
       
    )

    def __init__(self, user=None, role=None, type_=None, resource_id=None,
                 role_id=None, type_id=None, user_id=None):
        if user:
            self.user = user
        if user_id is not None:
            self.user_id = user_id
        if role:
            self.role = role
        if role_id is not None:
            self.role_id = role_id
        if type_:
            self.type = type_
        if type_id is not None:
            self.type_id = type_id
        self.resource_id = resource_id

    def __repr__(self) -> str:
        return (
            f'<Assignment type={self.type_id} '
            f'user={self.user_id} '
            f'role={self.role_id} '
            f'resource={self.resource_id}>'
        )