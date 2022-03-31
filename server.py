#!/usr/bin/env python3

# based off: https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
# Author: Ryan Clifford
# 2022-03-26

import sys
from httplib2 import UnimplementedDigestAuthOptionError
import bluetooth
import json
import data
import motor
SERVER_NAME = "Group 4"
print(SERVER_NAME)
UUID = "9f32d32e-e7b2-484b-819f-a571b8219a74"
print(UUID)
BUFSIZE = 4096
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.bind(("", bluetooth.PORT_ANY))
socket.listen(1)

port = socket.getsockname()[1]

bluetooth.advertise_service(socket, SERVER_NAME, service_id=UUID,
                            service_classes=[UUID, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )
print("Service Started")
try:
    while True:
        client_sock, client_info = socket.accept()
        print("Connect to: ", client_info)
        MotorControl = motor.MotorController()
        if len(sys.argv) < 2:
            raise Exception("Provide current state of door (\"open\"/\"closed\")")
        currentState = sys.argv[1].lower()

        try:
            while True:
                # assume all data can be recieved at once
                data = client_sock.recv(BUFSIZE)
                if not data:
                    break
                #data = json.loads(data)
                if data == b"OPEN":
                    if currentState == "closed":
                        print(f"[{data}] Opening...")
                        MotorControl.open()
                        currentState = "open"
                elif data == b"CLOSE":
                    if currentState == "open":
                        print(f"[{data}] Closing...")
                        MotorControl.close()
                        currentState = "closed"
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
    print("Socket Closed")
