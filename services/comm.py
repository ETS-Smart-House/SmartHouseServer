import time
from serial import Serial
from services.temperature import get_current_temperature


def sendCom(command, pin, inputvalue, port, baudrate, timeout)
  arduino = serial.Serial(port, baudrate, timeout)
  strtuple = (command, str(pin), str(inputvalue))
  output = "-".join(strtuple)
  arduino.write(bytes(output, 'utf-8'))

def inputCom(port, baudrate, timeout)
  arduino = serial.Serial(port, baudrate, timeout)
  data = arduino.readline()
  return data
