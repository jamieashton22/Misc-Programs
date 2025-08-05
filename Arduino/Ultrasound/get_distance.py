import numpy as np
import serial
import serial.tools.list_ports
import sys
import time

# GETTING AND SELECTING PORT - (or use 'ls /dev/tty.*' in terminal)

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
port = 'temp'
portList = []

print("\n List of available ports \n ")
for onePort in ports:
    portList.append(str(onePort.device))
    print(str(onePort))

port = input("\n select port e.g '/dev/.....' : \n")

if port not in portList:
    print("Invalid port chosen")
    sys.exit(1)

print ("\n Port selected: ")
print(port)


# GET BAUD RATE FROM USER

chosenBaud = input("\n Select Baud rate: \n")       # user input baud rate - check match arduino serial
serialInst.baudrate = chosenBaud

# OPEN PORT

serialInst.port = port
serialInst.open()
print("\n Port open \n")

data =[]

# GET RUNTIME FROM USER

time_to_run = int(input("\nSelect runtime in seconds: "))
start_time = time.time()

# GET THE DATA

while True:
    current_time = time.time()
    time_elapsed = current_time - start_time

    if time_elapsed > time_to_run:
        print("\n Complete")
        break

    if serialInst.in_waiting:
        packet = serialInst.readline()
        print(packet.decode('utf-8'))