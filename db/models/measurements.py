from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, Enum
from sqlalchemy_serializer import SerializerMixin

from db.connection import Base


class Measurement(Base, SerializerMixin):
    # set the name of table:
    __tablename__ = 'measurements'

    serialize_only = ('time', 'location', 'temperature', 'humidity')

    # set the structure of table:
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.utcnow)
    location = Column(Enum('floor1', 'floor2', 'outdoor'))
    temperature = Column(Float)
    humidity = Column(Float)
