from datetime import datetime
from dateutil.parser import parse
from db.connection import session
from db.models.temperature import Temperature, TemperaturePeriod

temperatures = {}


def set_temperature_service(session, payload):
    day = parse(payload['day']).date()
    floor = int(payload['floor'])

    temperature_entry = session.query(Temperature).filter_by(day=day).one_or_none()
    if not temperature_entry:
        temperature_entry = Temperature()
        temperature_entry.day = day
        temperature_entry.floor = floor

    if 'mode' in payload:
        temperature_entry.mode = payload['mode']

    if 'value' in payload:
        temperature_entry.value = payload['value']

    session.add(temperature_entry)
    session.commit()

    session.query(TemperaturePeriod).filter_by(day=temperature_entry.day).delete()

    if 'periods' in payload:
        for period in payload['periods']:
            period_entry = TemperaturePeriod()
            period_entry.day = temperature_entry.day
            period_entry.time_from = parse(period['from']).time()
            period_entry.time_to = parse(period['to']).time()
            period_entry.value = float(period['value'])
            session.add(period_entry)

    session.commit()

    send_temperature_to_node()

    return temperature_entry.to_dict()


def get_temperature_service(session, day, floor, time):
    try:
        day = parse(day).date()
    except:
        None
    try:
        time = parse(time).time()
    except:
        None

    temperature_entry = session.query(Temperature).filter_by(day=day).one_or_none()
    if not temperature_entry:
        return {
            'mode': 'off',
            'temperature': 'off'
        }

    mode = temperature_entry.mode

    # Auto
    if mode == 'auto':
        return {
            'mode': mode,
            'temperature': temperature_entry.value
        }

    query = session.query(TemperaturePeriod) \
        .filter_by(day=day) \
        .filter(time >= TemperaturePeriod.time_from) \
        .filter(time < TemperaturePeriod.time_to)

    temperature = query.one_or_none()

    return {
        'mode': mode,
        'temperature': temperature.value if temperature is not None else 'off'
    }


def get_current_temperature(floor):
    now = datetime.now()  # time object

    day = now.date()
    time = now.time()

    return get_temperature_service(session, day, floor, time)


def send_temperature_to_node():
    floor = '0'
    response = get_current_temperature(floor)
    mode = response['mode']
    temperature = response['temperature']
    command_string = f'{floor}-{mode}-{temperature}'
    # @TODO

    floor = '1'
    response = get_current_temperature(floor)
    mode = response['mode']
    temperature = response['temperature']
    command_string = f'{floor}-{mode}-{temperature}'


    # @TODO
