from datetime import date
from datetime import datetime

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

    # - Get current time and current temperature
    # - Send it to the heater

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

    temperature = None
    # if period not in temperatures[day][floor]['periods']:
    #     temperature = 0
    # else:
    #     temperature = temperatures[day][floor]['periods'][period]

    return {
        'mode': mode,
        'temperature': temperature
    }


def get_current_temperature(floor):
    now = datetime.now()  # time object

    date = str(now.date())

    bool = True