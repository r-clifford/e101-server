#!/usr/bin/env python3

# based off: https://github.com/pybluez/pybluez/blob/master/examples/simple/rfcomm-server.py
# Author: Ryan Clifford
# 2022-03-26

from datetime import datetime
import sys
from typing import List
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
currentState = sys.argv[1].lower()

DEBUG_MODE = False
if len(sys.argv) > 2:
    if sys.argv[2].lower() == "debug":
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
motorLock = Lock()
if not DEBUG_MODE:
    MotorControl = motor.MotorController(currentState=currentState)
    logging.info("Motor Controller Initialized")


schedulerThreads: List[Thread] = []
try:
    while True:
        client_sock, client_info = socket.accept()
        logging.info(f"Connect to: {client_info}")

        try:
            while True:
                data = client_sock.recv(BUFSIZE)
                if not data:
                    break
                logging.debug(f"RECV: {data}")

                if data == b"OPEN":
                    if currentState == "closed":

                        motorLock.acquire(blocking=True)
                        logging.info(f"[{data}] Opening...")
                        if not DEBUG_MODE:
                            MotorControl.open()
                        currentState = "open"
                        motorLock.release()

                    else:
                        logging.info("Door already open")
                elif data == b"CLOSE":
                    if currentState == "open":
                        motorLock.acquire(blocking=True)
                        logging.info(f"[{data}] Closing...")
                        if not DEBUG_MODE:
                            MotorControl.close()
                            currentState = "closed"
                        motorLock.release()
                    else:
                        logging.info("Door already closed")
                elif data.decode().split(";")[0] == "SCHED":
                    schedule_input = data.decode().split(";")
                    logging.debug(f"SCHED Case: {schedule_input}")
                    logging.info(schedule_input)
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
                    schedulerThreads.append(scheduler.start())
                    schedulerThreads[-1].start()
                    logging.info(f"Started scheduler")
                elif data == b"CANCEL":
                    logging.info(f"[{data}] Canceling...")
                    logging.info(f"Found {len(schedulerThreads)} running threads")
                    for thread in schedulerThreads:
                        thread.join(
                            timeout=1
                        )  # block until thread completes or 1 sec passes
                        logging.info(f"Thread destroyed")
                else:
                    logging.info(f"Unknown data: {data}")
        except OSError:
            logging.critical("OS ERROR")
        except UnboundLocalError:
            logging.error(f"Motor controller likely unbound: DEBUG == {DEBUG_MODE}")
        logging.info("Client Disconnected")

        client_sock.close()
except KeyboardInterrupt:
    socket.close()
    logging.info("\nSocket Closed")
