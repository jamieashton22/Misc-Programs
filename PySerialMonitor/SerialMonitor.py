import numpy as np
import serial
import serial.tools.list_ports
import sys
import time

#------ GET AND SELECT PORT ----------------------------------------

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
port = ''
portList = []

print("\n List of available ports \n")
for onePort in ports:
    portList.append(str(onePort.device))
    print(str(onePort))

port = input("\n select port \n")

if port not in portList:
    print("Invalid port chosen")
    sys.exit(1)

print("\n Port selected: ")
print(port)

# OPEN PORT

#get baud rate from user
chosenBaud = input("\n select baud rate \n")
serialInst.baudrate = chosenBaud

serialInst.port = port
serialInst.open()
print("\n port open \n")

# ---------------------------------------------------------------------

# # GET RUNTIME FROM USER

# time_to_run = int(input("\nselect runtime in seconds: "))
# start_time = time.time()

# # GET THE DATA

# while True:
#     current_time = time.time()
#     time_elapsed = current_time - start_time

#     if time_elapsed > time_to_run:ç
#         print("\n complete")

# ---------------------------------------------------------------------

while True:

    if serialInst.in_waiting:

        data_raw = serialInst.readline()
        data_strip=data_raw.decode('utf-8').rstrip()
        print(data_strip)
