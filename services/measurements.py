from db.models.measurements import Measurement


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

# def get_measurement_service(session, time, location):
#     """
#
#     :param session:
#     :param time: either a day or a from:to format
#     :param location:
#     :return:
#     """
