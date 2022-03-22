from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    '{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}'.format(
        dialect='mysql',
        driver='pymysql',
        user='smart_home_user',
        password='smart_home_password',
        host='localhost',
        port=8010,
        database='smart_home'
    ), echo=True
)

Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()
