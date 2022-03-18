from sqlalchemy import String, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Light(Base):
    __tablename__ = 'light'

    room_id = Column(String, primary_key=True)

    value = Column(String)