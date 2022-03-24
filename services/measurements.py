from sqlalchemy import func

from db.models.measurements import Measurement
from services.comm import send_command
from services.comm import input_command

def request_mesurment(ID, mode=0):
    send_command("RS", ID,  mode)
    in_string = input_command().decode('utf-8')
    print(in_string)


def set_measurement_service(session, temperature, humidity, location):
    """
    :param session:
    :param temperature: Float
    :param humidity: Float
    :param location: ENUM('indoor', 'outdoor')
    :return:
    """
    measurement = Measurement()
    measurement.temperature = temperature
    measurement.humidity = humidity
    measurement.location = location
    session.add(measurement)
    session.commit()

    return measurement


def get_measurement_service(session, location):
    results = session.query(Measurement) \
        .filter_by(location=location) \
        .with_entities(func.date(Measurement.time).label('date'),
                       func.round(func.avg(Measurement.temperature), 0).label('temperature'),
                       func.round(func.avg(Measurement.humidity), 0).label('humidity')) \
        .group_by(func.date(Measurement.time)).all()

    return list(
        map(lambda result: {'date': str(result.date), 'temperature': result.temperature, 'humidity': result.humidity},
            results))
