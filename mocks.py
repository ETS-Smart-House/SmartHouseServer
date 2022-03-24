import random
from datetime import datetime
from datetime import timedelta
from random import uniform
from dateutil.parser import parse

from db.connection import session
from db.models.measurements import Measurement
from db.models.temperature import Temperature, TemperaturePeriod


def mock_measurements():
    start_date = parse('2022-03-21T00:00:00Z')

    dates = []
    for day_add in range(0, 60):
        d = start_date + timedelta(days=day_add)
        for minute_add in range(0, 288):
            m = d + timedelta(minutes=minute_add)
            dates.append(m)
            measurement = Measurement()
            measurement.temperature = round(uniform(0, 35))
            measurement.humidity = round(uniform(0, 35))
            measurement.location = 'indoor'
            measurement.time = m
            session.add(measurement)

    session.commit()


def mock_temperatures():
    start_date = parse('2022-03-21T00:00:00Z')
    for floor in range(0, 2):
        for day_add in range(0, 60):
            d = start_date + timedelta(days=day_add)

            temperature = Temperature()
            temperature.day = d
            temperature.floor = floor
            temperature.mode = random.choice(['auto', 'manual'])
            temperature.value = round(uniform(0, 35))
            session.add(temperature)
            session.commit()

            time_to = d
            for hour_add in range(2, 24, 2):
                time_from = time_to
                time_to = time_to + timedelta(hours=2)
                temperature_period = TemperaturePeriod()
                temperature_period.parent = temperature.id
                temperature_period.time_from = time_from
                temperature_period.time_to = time_to
                temperature_period.value = round(uniform(0, 35))
                session.add(temperature_period)
            session.commit()


# mock_measurements()
mock_temperatures()
