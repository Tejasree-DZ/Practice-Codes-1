
from controls import SessionLocal
from models import Role, User, Pool, Organization

session = SessionLocal()


role_data = [
    {"name": "Admin", "admin": True, "manager": False, "user": False},
    {"name": "Manager", "admin": False, "manager": True, "user": False},
    {"name": "User", "admin": False, "manager": False, "user": True}
]

for r in role_data:
    existing_role = session.query(Role).filter_by(name=r["name"]).first()
    if not existing_role:
        session.add(Role(**r))

session.commit()


user_data = [
    {"name": "Alice", "password": "alice123", "mail": "alice@mail.com", "mobile": "1234567890"},
    {"name": "Bob", "password": "bob123", "mail": "bob@mail.com", "mobile": "0987654321"},
    {"name": "Kin", "password": "kin123", "mail": "kin@mail.com", "mobile": "4545667899"},
]

for u in user_data:
    existing_user = session.query(User).filter_by(mail=u["mail"]).first()
    if not existing_user:
        session.add(User(**u))

session.commit()

main_pool = session.query(Pool).filter_by(name="Main Pool").first()

if not main_pool:
    main_pool = Pool(name="Main Pool")
    session.add(main_pool)
    session.commit()

users = session.query(User).all()
roles = session.query(Role).all()

def upsert_organization(name, user_id, role_id, pool_id):

    existing_org = session.query(Organization).filter_by(
        name=name,
        user_id=user_id,
        role_id=role_id
    ).first()

    if existing_org:
        
        existing_org.pool_id = pool_id
        print("Organization updated")
    else:
        
        new_org = Organization(
            name=name,
            user_id=user_id,
            role_id=role_id,
            pool_id=pool_id
        )
        session.add(new_org)
        print("Organization inserted")

    session.commit()

upsert_organization(
    name="DigiOrg",
    user_id=users[0].id,
    role_id=roles[0].id,
    pool_id=main_pool.id
)
org1 = Organization(
    name="Digiorg",
    user_id=users[0].id,
    role_id=roles[0].id,
    pool_id=main_pool.id
)
org2 = Organization(
    name="Digiorg",
    user_id=users[0].id,
    role_id=roles[0].id,
    pool_id=main_pool.id
)

session.add(org1)
session.add(org2)

try:
    session.commit()
except Exception as e:
    session.rollback()
print("Data inserted/updated successfully in TiDB!")

session.close()