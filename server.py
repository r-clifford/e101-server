#!/usr/bin/env python3

# based off: https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
# Author: Ryan Clifford
# 2022-03-26

from httplib2 import UnimplementedDigestAuthOptionError
import bluetooth
import json
import data
import motor
SERVER_NAME = "Group 4"
UUID = ""
BUFSIZE = 4096
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.bind(("", bluetooth.PORT_ANY))
socket.listen(1)

port = socket.getsockname()[1]


bluetooth.advertise_service(socket, SERVER_NAME, service_id=UUID,
                            service_classes=[UUID, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )


client_sock, client_info = socket.accept()
print("Connect to: ", client_info)
MotorControl = motor.MotorController()
try:
    while True:
        # assume all data can be recieved at once
        data = client_sock.recv(BUFSIZE)
        if not data:
            break
        data = json.loads(data)
        if data.Command != "KEEP_ALIVE":
            if data.Command == "OPEN":
               MotorControl.open()
               client_sock.send(json.dumps({"RESP": "OPEN"}))
            elif data.Command == "CLOSE":
                MotorControl.close()
                client_sock.send(json.dumps({"RESP": "CLOSED"}))
            elif data.Command == "SCHED":
                raise NotImplementedError
except OSError:
    pass

print("Client Disconnected")

client_sock.close()
socket.close()
