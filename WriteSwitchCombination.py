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


ser = serial.Serial(port, chosenBaud )
time.sleep(2)

while True:
    command = input(">> ").strip()
    if len(command) == 6:
        ser.write((command + '\n').encode())
    else:
        print("Invalid command length ")

    time.sleep(0.1)
    while ser.in_waiting:
        response = ser.readline().decode().strip()
        if response:
            print("[Arduino] " + response)