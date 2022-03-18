from flask import Flask, request
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert

from models import Light

app = Flask(__name__)

engine = create_engine('mysql://smart_home_user:smart_home_password@localhost:8001/smart_home')

light = {}
temperature = {}


@app.get("/light")
def get_lights():
    return light


@app.post('/light')
def set_lights():
    body = request.get_json()
    room, value = body['id'], int(body['value'])
    light[room] = value

    transaction = insert(Light).values(id=room, value=value)
    engine.execute(transaction)

    return light


@app.get('/temperature')
def get_temperature():
    args = request.args
    date_from = args.get('from')
    date_to = args.get('to')
    if date_from:
        date_from = parse(date_from)
    if date_to:
        date_to = parse(date_to)

    return {
        'date_from': date_from,
        'date_to': date_to
    }
