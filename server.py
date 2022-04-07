#!/usr/bin/env python3

# based off: https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
# Author: Ryan Clifford
# 2022-03-26

from datetime import datetime
import sys
import bluetooth
import motor
import logging
import schedule
from threading import Thread, Lock

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
if len(sys.argv) < 2:
    logging.critical("Current door state not provided")
    raise Exception('Provide current state of door ("open"/"closed")')
DEBUG_MODE = False
if len(sys.argv) > 2:
    if sys.argv[2].lower() == "DEBUG":
        DEBUG_MODE = True
        print("In debugging mode, will not call motor control")
        logging.info("Started in Debug Mode")

SERVER_NAME = "Group 4"
logging.info(f"Server name: {SERVER_NAME}")
UUID = "9f32d32e-e7b2-484b-819f-a571b8219a74"
logging.info(f"Service UUID: {UUID}")
BUFSIZE = 4096
logging.info(f"RECV BUFFSIZE: {BUFSIZE}")
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
logging.info("Bluetooth Service Started")
currentState = sys.argv[1].lower()
motorLock = Lock()
if not DEBUG_MODE:
    MotorControl = motor.MotorController(currentState=currentState)
    logging.info("Motor Controller Initialized")


currentTime = datetime.now()
try:
    while True:
        client_sock, client_info = socket.accept()
        logging.info(f"Connect to: {client_info}")

        try:
            while True:
                # assume all data can be recieved at once
                data = client_sock.recv(BUFSIZE)
                if not data:
                    break
                # data = json.loads(data)
                if data == b"OPEN":
                    if currentState == "closed":
                        with motorLock:
                            logging.info(f"[{data}] Opening...")
                            if not DEBUG_MODE:
                                MotorControl.open()
                            currentState = "open"
                    else:
                        logging.info("Door already open")
                elif data == b"CLOSE":
                    if currentState == "open":
                        with motorLock:
                            logging.info(f"[{data}] Closing...")
                            if not DEBUG_MODE:
                                MotorControl.close()
                                currentState = "closed"
                            else:
                                logging.info("Door already closed")
                elif str(data).split(";")[0] == "SCHED":
                    logging.error(f"Scheduling not implemented: [{data}]")
                    schedule_input = str(data).split(";")
                    if len(schedule_input) < 4:
                        logging.error(f"Schedule called with data: {data}")
                    scheduler = schedule.Scheduler(
                        MotorControl,
                        motorLock,
                        schedule_input[1],
                        schedule_input[2],
                        schedule_input[3],
                        currentState,
                    )
                    scheduler.start().start()
                    # raise NotImplementedError
                else:
                    logging.info(f"Unknown data: {data}")
        except OSError:
            pass

        logging.info("Client Disconnected")

        client_sock.close()
except KeyboardInterrupt:
    socket.close()
    logging.info("\nSocket Closed")
