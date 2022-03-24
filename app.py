from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from services.lights import set_lights_service, get_lights_service
from services.measurements import get_measurement_service, request_mesurment
from services.temperature import get_temperature_service, set_temperature_service, get_current_temperature, \
    send_temperature_to_node
from threading import Timer
from db.connection import session



TIMER_INTERVAL = 60 * 5  # 60s * 5

app = Flask(__name__)
CORS(app)


@app.route("/light", methods=['GET'])
def get_lights():
    lights = get_lights_service()

    return jsonify(lights)


@app.route("/light", methods=['POST'])
def set_lights():
    body = request.get_json()
    if 'room' not in body:
        raise Exception()
    if 'value' not in body:
        raise Exception()

    lights = set_lights_service(body)

    return jsonify(lights)


@app.route('/temperature', methods=['GET'])
def get_temperature():
    args = request.args
    day = args.get('day')
    if not day:
        raise Exception('Query parameter `day` is missing')

    temperature = get_temperature_service(session, day)

    return jsonify(temperature)


@app.route('/temperature', methods=['POST'])
def set_temperature():
    body = request.get_json()

    temperature = set_temperature_service(session, body)

    return jsonify(temperature)


@app.route('/measurements', methods=['GET'])
def get_measurements():
    args = request.args

    location = args.get('location')
    if not location:
        raise Exception('Query parameter `location` is missing')

    measurements = get_measurement_service(session, location)

    return jsonify(measurements)

    
