import serial

'''
Heating : command = "H" pin=9 inputvalue=1/0 Output: "H-9-0"
Light: command = "L" pin=2 inputvalue=1-100 Output: "L-2-45"
Pump: command="P" pin=12 inputvalue=1/0 Output: "P-12-1"
'''


def send_command(command, pin, inputvalue, port="/dev/ttyUSB0", baudrate=115200, timeout=0.1):
    arduino = serial.Serial(port, baudrate, timeout)
    strtuple = (command, str(pin), str(inputvalue))
    output = "-".join(strtuple)
    arduino.write(bytes(output, 'utf-8'))


def input_command(port="/dev/ttyUSB0", baudrate=115200, timeout=0.1):
    arduino = serial.Serial(port, baudrate, timeout)
    data = arduino.readline()

    return data
