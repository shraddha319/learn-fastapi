from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

# create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create SessionLocal class
# instance of this will be a db session
# 'Local' to differentiate from sqlAlchemy's Session class
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base class
# from this all orms models are inherited
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi-course', user='postgres', password='shraddha###', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('database connected successfully')
#         break
#     except Exception as error:
#         print('Error:', error)
#         time.sleep(2)