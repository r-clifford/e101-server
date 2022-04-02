#!/usr/bin/env python3

# based off: https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
# Author: Ryan Clifford
# 2022-03-26

import sys
import bluetooth
import motor
if len(sys.argv) < 2:
    raise Exception('Provide current state of door ("open"/"closed")')
DEBUG_MODE = False
if len(sys.argv) > 2:
    if sys.argv[2].lower() == "DEBUG":
        DEBUG_MODE = True
        print("In debugging mode, will not call motor control")

SERVER_NAME = "Group 4"
print(SERVER_NAME)
UUID = "9f32d32e-e7b2-484b-819f-a571b8219a74"
print(UUID)
BUFSIZE = 4096
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.bind(("", bluetooth.PORT_ANY))
socket.listen(1)

port = socket.getsockname()[1]

bluetooth.advertise_service(
    socket,
    SERVER_NAME,
    service_id=UUID,
    service_classes=[UUID, bluetooth.SERIAL_PORT_CLASS],
    profiles=[bluetooth.SERIAL_PORT_PROFILE],
)
print("Bluetooth Service Started")
if not DEBUG_MODE:
    MotorControl = motor.MotorController()
    print("Motor Controller Initialized")
try:
    while True:
        client_sock, client_info = socket.accept()
        print("Connect to: ", client_info)

        currentState = sys.argv[1].lower()

        try:
            while True:
                # assume all data can be recieved at once
                data = client_sock.recv(BUFSIZE)
                if not data:
                    break
                # data = json.loads(data)
                if data == b"OPEN":
                    if currentState == "closed":
                        print(f"[{data}] Opening...")
                        if not DEBUG_MODE:
                            MotorControl.open()
                        currentState = "open"
                    else:
                        print("Door already open")
                elif data == b"CLOSE":
                    if currentState == "open":
                        print(f"[{data}] Closing...")
                        if not DEBUG_MODE:
                            MotorControl.close()
                        currentState = "closed"
                    else:
                        print("Door already closed")
                elif data == b"SCHED":
                    print(f"Scheduling not implemented: [{data}]")
                    # raise NotImplementedError
                else:
                    print(f"Unknown data: {data}")
        except OSError:
            pass

        print("Client Disconnected")

        client_sock.close()
except KeyboardInterrupt:
    socket.close()
    print("\nSocket Closed")
