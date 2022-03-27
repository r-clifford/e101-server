#!/usr/bin/env python3

# based off: https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
# Author: Ryan Clifford
# 2022-03-26

import bluetooth
import json
import data
import motor
SERVER_NAME = "Group 4"
UUID = ""
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

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print(data)
except OSError:
    pass

print("Client Disconnected")

client_sock.close()
socket.close()
