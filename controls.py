from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_USER = "EfuwPUKvJ5RpMJF.root"
DB_PASSWORD = "FH19VAICz8T0yN6N"
DB_HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
DB_PORT = 4000
DB_NAME = "mydatabase"
CA_PATH = "C:/Users/Teja Sree/Downloads/isrgrootx1.pem"


engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={CA_PATH}",
    echo=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW();"))  # Use text() in SQLAlchemy 2.x
            print("Connection successful! Current DB time:", result.fetchone()[0])
    except Exception as e:
        print("Connection failed:", e)