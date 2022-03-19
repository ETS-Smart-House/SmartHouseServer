lights = {}


def set_lights_service(payload):
    room, value = payload['id'], int(payload['value'])
    lights[room] = value

    send_light_to_node(room, value)

    return lights


def get_lights_service():
    return lights

def send_light_to_node(room, value):
    command_string = f'{room}-{value}'

    # @TODO
