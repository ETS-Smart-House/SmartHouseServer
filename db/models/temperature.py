from sqlalchemy import Column, Integer, Date, Float, ForeignKey, DateTime, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from db.connection import Base


class TemperaturePeriod(Base, SerializerMixin):
    __tablename__ = 'temperature_period'

    serialize_only = ('time_from', 'time_to', 'value')

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_from = Column(Time)
    time_to = Column(Time)
    value = Column(Float)
    day = Column(Date, ForeignKey('temperature.day'))


class Temperature(Base, SerializerMixin):
    # set the name of table:
    __tablename__ = 'temperature'

    serialize_only = ('day', 'floor', 'mode', 'value', 'periods')

    # set the structure of table:
    day = Column(Date, primary_key=True)
    floor = Column(Integer)
    mode = Column(String(6))
    value = Column(Float)
    periods = relationship(TemperaturePeriod)
