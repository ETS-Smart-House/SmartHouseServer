from datetime import datetime
from dateutil.parser import parse

temperatures = {}


def set_temperature_service(payload):
    day = payload['day']
    floor = str(payload['floor'])

    if day not in temperatures:
        temperatures[day] = {}
    if floor not in temperatures[day]:
        temperatures[day][floor] = {}

    if 'mode' in payload:
        temperatures[day][floor]['mode'] = payload['mode']

    if 'value' in payload:
        temperatures[day][floor]['auto_value'] = payload['value']

    if 'periods' in payload:
        temperatures[day][floor]['periods'] = payload['periods']

    send_temperature_to_node()

    return temperatures[day]


def get_temperature_service(day, floor, time_from, time_to):
    if day not in temperatures:
        raise Exception(f'Day {day} not configured')

    if floor not in temperatures[day]:
        raise Exception(f'Floor {floor} not configured for day {day} not configured')

    mode = temperatures[day][floor]['mode']

    # Auto
    if mode == 'auto':
        temperature = temperatures[day][floor]['auto_value']
        return {
            'mode': mode,
            'temperature': temperature
        }

    # Periodical
    if 'periods' not in temperatures[day][floor]:
        raise Exception(f'No periods configured for day {day}')

    periods = temperatures[day][floor]['periods']

    temperature = 'off'

    for period in periods:
        period_from = parse(period['from'])
        period_to = parse(period['to'])
        requested_from = parse(time_from)
        requested_to = parse(time_to)
        if requested_from >= period_from and requested_to <= period_to:
            temperature = period['value']
            break

    return {
        'mode': mode,
        'temperature': temperature
    }


def get_current_temperature(floor):
    now = datetime.now()  # time object

    day = str(now.date())

    if day not in temperatures or floor not in temperatures[day]:
        return 'off'

    if temperatures[day][floor]['mode'] == 'auto':
        return temperatures[day][floor]['value']

    periods = temperatures[day][floor]['periods']

    for period in periods:
        period_from = parse(period['from'])
        period_to = parse(period['to'])
        if period_from <= now <= period_to:
            return period['value']

def send_temperature_to_node():
    floor = '0'
    temperature = get_current_temperature(floor)
    command_string = f'{floor}-{temperature}'
    # @TODO

    floor = '1'
    temperature = get_current_temperature(floor)
    command_string = f'{floor}-{temperature}'

    # @TODO