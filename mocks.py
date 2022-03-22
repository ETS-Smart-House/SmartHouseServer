from datetime import datetime
from datetime import timedelta
from random import uniform
from dateutil.parser import parse

from db.connection import session
from db.models.measurements import Measurement


def mock_measurements():
    start_date = parse('2022-03-21T00:00:00Z')

    dates = []
    for day_add in range(0, 20):
        d = start_date + timedelta(days=day_add)
        for minute_add in range(0, 288):
            m = d + timedelta(minutes=minute_add)
            dates.append(m)
            measurement = Measurement()
            measurement.temperature = uniform(0, 35)
            measurement.humidity = uniform(0, 35)
            measurement.location = 'indoor'
            measurement.time = m
            session.add(measurement)

    session.commit()


mock_measurements()
