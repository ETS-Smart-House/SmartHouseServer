import time
from serial
from services.temperature import get_current_temperature


def sendCom(command, pin, inputvalue, port="/dev/ttyUSB0", baudrate=115200, timeout=0.1)
  arduino = serial.Serial(port, baudrate, timeout)
  strtuple = (command, str(pin), str(inputvalue))
  output = "-".join(strtuple)
  arduino.write(bytes(output, 'utf-8'))

def inputCom(port="/dev/ttyUSB0", baudrate=115200, timeout=0.1)
  arduino = serial.Serial(port, baudrate, timeout)
  data = arduino.readline()
  
  return data
