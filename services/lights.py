from db.models.light import Light


def set_lights_service(session, payload):
    room, value = payload['room'], int(payload['value'])
    light = session.query(Light) \
        .filter_by(room=room) \
        .one_or_none()

    if not light:
        light = Light()
        light.room = room

    light.value = value

    session.add(light)
    session.commit()

    send_light_to_node(room, value)

    return light.to_dict()


def get_lights_service(session):
    lights = session.query(Light).all()

    lights = list(map(lambda light: light.to_dict(), lights))

    return lights


def send_light_to_node(room, value):
    command_string = f'{room}-{value}'

    # @TODO
