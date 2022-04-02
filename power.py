#!/usr/bin/env python3
from gpiozero import Button
from signal import pause
import os, sys
import logging

offGPIO = 21
holdTime = 3
logging.basicConfig(
    filename="/home/pi/power.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)

logging.info(f"Pin: {offGPIO}")
logging.info(f"Required hold time {holdTime}")
# the function called to shut down the RPI
def shutdown():
    logging.info(f"Shutting down...")
    os.system("sudo poweroff")


btn = Button(offGPIO, hold_time=holdTime)
btn.when_held = shutdown
pause()
