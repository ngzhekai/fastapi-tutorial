from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 依赖关系
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 使用 psycopg2 模组（驱动）来写SQL代码 来跟数据库沟通
# 毕竟都使用SQLAlchemy （利用python 语言写SQL） 来完成沟通
# while True:
#     try:
#         conn = psycopg2.connect(
#             "host=localhost dbname=fastapi user=postgres password=1234 port=5432")
#         cur = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
