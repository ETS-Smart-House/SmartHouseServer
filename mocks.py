import random
from datetime import timedelta, time, datetime
from random import uniform

from db.connection import session
from db.models.measurements import Measurement
from db.models.temperature import Temperature, TemperaturePeriod

start_date = datetime.now()


def mock_measurements():
    dates = []
    for location in ['indoor', 'outdoor']:
        for day_add in range(0, 20):
            d = start_date - timedelta(days=day_add)
            for minute_add in range(0, 288, 2):
                m = d + timedelta(minutes=minute_add)

                if day_add < 10:
                    temperature_value = round(uniform(15, 35))
                    humidity_value = round(uniform(0, 50))
                else:
                    temperature_value = round(uniform(0, 15))
                    humidity_value = round(uniform(50, 100))

                dates.append(m)
                measurement = Measurement()
                measurement.temperature = temperature_value
                measurement.humidity = humidity_value
                measurement.location = location
                measurement.time = m
                session.add(measurement)

        session.commit()


def mock_temperatures():
    for floor in range(0, 2):
        for day_add in range(-10, 10):
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
                temperature_value = 0
                if hour_add % 2 is 0:
                    temperature_value = round(uniform(15, 35))
                else:
                    temperature_value = round(uniform(0, 15))

                time_from = time_to
                time_to = time_to + timedelta(hours=2)
                temperature_period = TemperaturePeriod()
                temperature_period.parent = temperature.id
                temperature_period.time_from = time_from
                temperature_period.time_to = time_to
                temperature_period.value = temperature_value
                session.add(temperature_period)
            session.commit()


mock_measurements()
mock_temperatures()
