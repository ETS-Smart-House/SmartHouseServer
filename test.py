import serial
import time
arduino = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
arduino.write(bytes("RS-0-0", "utf-8"))
print('test')
print(arduino.readline())
