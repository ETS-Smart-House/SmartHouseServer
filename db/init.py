from sqlalchemy.orm import declarative_base

from db.connection import engine, Base
from db.models.light import Light
from db.models.temperature import Temperature, TemperaturePeriod
from db.models.measurements import Measurement

Base.metadata.create_all(engine)
