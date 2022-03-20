from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy_serializer import SerializerMixin

from db.connection import Base


class Light(Base, SerializerMixin):
    # set the name of table:
    __tablename__ = 'light'

    serialize_only = ('room', 'value')

    # set the structure of table:
    room = Column(String(20), primary_key=True)
    value = Column(Integer())
