from db.models.light import Light
from services.comm import send_command
from services.comm import input_command

from services.measurements import request_mesurment
import time

lights = {}


def set_lights_service(payload):
    room, value = payload['room'], int(payload['value'])
    lights[room] = value

    send_light_to_node(room, value)

    return lights


def get_lights_service():
    return lights


def send_light_to_node(room, value):
    if room == "stairs":
        pin = 2
    elif room == "room1":
        pin = 3
    elif room == "room2":
        pin = 4
    elif room == "living-room":
        pin = 5 
    elif room == "bathroom":
        pin = 6
    send_command("L", pin, value)
    print(input_command())
    time.sleep(1)
    request_mesurment(0, 0)
