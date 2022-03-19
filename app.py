from flask import Flask, request

from services.lights import set_lights_service, get_lights_service
from services.temperature import get_temperature_service, set_temperature_service, get_current_temperature, \
    send_temperature_to_node
from threading import Timer

TIMER_INTERVAL = 60 * 5  # 60s * 5

app = Flask(__name__)


@app.get("/light")
def get_lights():
    lights = get_lights_service()

    return lights


@app.post('/light')
def set_lights():
    body = request.get_json()
    if 'id' not in body:
        raise Exception()
    if 'value' not in body:
        raise Exception()

    lights = set_lights_service(body)

    return lights


@app.get('/temperature')
def get_temperature():
    args = request.args
    day = args.get('day')
    if not day:
        raise Exception('Query parameter `day` is missing')

    floor = str(args.get('floor'))
    if floor not in ['0', '1']:
        raise Exception('Value `floor` is missing or wrong')

    time_from = args.get('time_from')
    if not time_from:
        raise Exception('Query parameter `time_from` is missing')

    time_to = args.get('time_to')
    if not time_to:
        raise Exception('Query parameter `time_to` is missing')

    temperature = get_temperature_service(day, floor, time_from, time_to)

    return temperature


@app.post('/temperature')
def set_temperature():
    body = request.get_json()

    if 'day' not in body:
        raise Exception('Value `day` is missing')

    if 'mode' not in body or (body['mode'] not in ['auto', 'manual']):
        raise Exception('Value `mode` is missing or wrong')

    if 'floor' not in body or (str(body['floor']) not in ['0', '1']):
        raise Exception('Value `floor` is missing or wrong')

    temperature = set_temperature_service(body)

    return temperature


def get_temperature_interval():
    send_temperature_to_node()
    Timer(TIMER_INTERVAL, get_temperature_interval).start()


Timer(TIMER_INTERVAL, get_temperature_interval).start()  # after 30 seconds, "hello, world" will be printed
