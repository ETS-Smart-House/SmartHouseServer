from sqlalchemy.orm import declarative_base

from db.connection import engine, Base
from db.models.light import Light
from db.models.temperature import Temperature, TemperaturePeriod

Base.metadata.create_all(engine)
