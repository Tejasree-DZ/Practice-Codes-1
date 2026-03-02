from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from controls import engine, SessionLocal

Base = declarative_base()  


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    admin = Column(Boolean, default=False)
    manager = Column(Boolean, default=False)
    user = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    password = Column(String(100))
    mail = Column(String(100), unique=True)
    mobile = Column(String(20), unique=True)


class Pool(Base):
    __tablename__ = "pool"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey("pool.id"), nullable=True)
    sub_pools = relationship("Pool", backref="parent", remote_side=[id])


from sqlalchemy import UniqueConstraint

class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    pool_id = Column(Integer, ForeignKey("pool.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('name', 'user_id', 'role_id', name='unique_org_constraint'),
    )

    user = relationship("User")
    role = relationship("Role")
    pool = relationship("Pool")

    user = relationship("User")
    role = relationship("Role")
    pool = relationship("Pool")
if __name__ == "__main__":
    from controls import engine
    Base.metadata.create_all(bind=engine)