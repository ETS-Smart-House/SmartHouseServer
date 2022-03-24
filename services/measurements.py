from sqlalchemy import func

from db.models.measurements import Measurement
from db.connection import session
from services.comm import send_command
from services.comm import input_command

def request_mesurment(ID):
    send_command("RS", ID, 0)
    in_string = input_command().decode('utf-8')
    print(in_string)
    s_list = in_string.split("-")
    print(s_list)
    if s_list[1] == '0':
    	set_measurement_service(session, s_list[3], s_list[2], 'outdoor')
    else: 
    	set_measurement_service(session, s_list[3], s_list[2], 'indoor')

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
