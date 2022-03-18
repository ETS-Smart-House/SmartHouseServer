lights = {}

def set_lights_service(payload):
    room, value = payload['id'], int(payload['value'])
    lights[room] = value

    command_string = f'{room}:{value}'

    # @TODO

    return lights

def get_lights_service():
    return lights