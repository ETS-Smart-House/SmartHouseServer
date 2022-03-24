from sqlalchemy import Column, Integer, Date, Integer, ForeignKey, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from db.connection import Base


class TemperaturePeriod(Base, SerializerMixin):
    __tablename__ = 'temperature_period'

    serialize_only = ('time_from', 'time_to', 'value')

    id = Column(Integer, primary_key=True, autoincrement=True, )
    time_from = Column(Time)
    time_to = Column(Time)
    value = Column(Integer)
    parent = Column(Integer, ForeignKey('temperature.id'))


class Temperature(Base, SerializerMixin):
    # set the name of table:
    __tablename__ = 'temperature'

    serialize_only = ('day', 'floor', 'mode', 'value', 'periods')

    # set the structure of table:
    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(Date)
    floor = Column(Integer)
    mode = Column(String(6))
    value = Column(Integer)
    periods = relationship(TemperaturePeriod)
