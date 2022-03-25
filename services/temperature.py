from time import sleep

from datetime import datetime
from dateutil.parser import parse
from db.connection import session
from db.models.temperature import Temperature, TemperaturePeriod

from services.measurements import get_latest_measurement
from services.comm import send_command


def manage_temperature():
    floor1 = get_latest_measurement(session, "floor1")
    floor2 = get_latest_measurement(session, "floor2")
    temp1 = floor1['temperature']
    temp2 = floor2['temperature']
    targetTemp1 = get_current_temperature(0)[1]
    targetTemp2 = get_current_temperature(1)[1]
    print("real temp: " + str(temp1))
    print("real temp: " + str(temp2))
    print("target temp: " + str(targetTemp1))
    print("target temp: " + str(targetTemp2))
    if temp1 < targetTemp1:
        send_command("P", 0, 1)
    else:
        send_command("P", 0, 0)
    sleep(0.1)
    if temp2 < targetTemp2:
        send_command("P", 1, 1)
    else:
        send_command("P", 1, 0)


def set_temperature_service(session, payload):
    response = []
    for item in payload:
        if ('day' not in item) or ('floor' not in item) or ('mode' not in item) or ('value' not in item):
            continue

        day = parse(item['day']).date()
        floor = int(item['floor'])
        mode = item['mode']
        value = item['value']

        temperature_entry = session.query(Temperature).filter_by(floor=floor).filter_by(day=day).one_or_none()
        if not temperature_entry:
            temperature_entry = Temperature()
            temperature_entry.day = day
            temperature_entry.floor = floor
        temperature_entry.mode = mode
        temperature_entry.value = value

        session.add(temperature_entry)
        session.commit()

        session.query(TemperaturePeriod).filter_by(parent=temperature_entry.id).delete()

        if 'periods' in item:
            for period in item['periods']:
                period_entry = TemperaturePeriod()
                period_entry.parent = temperature_entry.id
                period_entry.time_from = parse(period['time_from']).time()
                period_entry.time_to = parse(period['time_to']).time()
                period_entry.value = period['value']
                session.add(period_entry)

            session.commit()
        response.append(temperature_entry.to_dict())

    send_temperature_to_node()

    return response


def get_temperature_service(session, day):
    day = parse(day).date()

    temperature_entries = session.query(Temperature).filter_by(day=day).all()
    if not temperature_entries:
        return {
            'mode': 'off',
            'temperature': 'off',
            'periods': []
        }

    return list(map(lambda temperature_entry: temperature_entry.to_dict(), temperature_entries))


def get_current_temperature(floor):
    now = datetime.now()  # time object

    day = now.date()
    time = now.time()

    temperature_entry = session.query(Temperature).filter_by(floor=floor).filter_by(day=day).one_or_none()
    if not temperature_entry:
        return None

    period = session.query(TemperaturePeriod) \
        .filter_by(parent=temperature_entry.id) \
        .filter(time > TemperaturePeriod.time_from) \
        .filter(time < TemperaturePeriod.time_to) \
        .one_or_none()

    if not period:
        return None

    return temperature_entry.mode, period.value


def send_temperature_to_node():
    floor = '0'
    mode, temperature = get_current_temperature(floor)
    command_string = f'{floor}-{mode}-{temperature}'
    # @TODO

    floor = '1'
    mode, temperature = get_current_temperature(floor)
    command_string = f'{floor}-{mode}-{temperature}'

    # @TODO
