# Author: Ryan Clifford
# 2022-03-26
import gpiozero
import os
import time


class MotorController:
    OPEN_VALUE = 1
    CLOSE_VALUE = -1
    RUN_TIME = 3
    current_status = ""

    def __init__(
        self,
        currentState,
        gpio_pin=17,
        min_pulse_width=0.001,
        max_pulse_width=0.002,
        frame_width=0.020,
    ) -> None:
        os.system("sudo pigpiod")
        gpiozero.Device.pin_factory = gpiozero.pins.pigpio.PiGPIOFactory()
        self.motor = gpiozero.Servo(
            pin=gpio_pin,
            initial_value=0,
            min_pulse_width=min_pulse_width,
            max_pulse_width=max_pulse_width,
            frame_width=frame_width,
        )
        self.current_status = currentState

    def Pin(self):
        return self.motor.pin

    def Value(self):
        return self.motor.value

    def __set_value(self, value):
        self.motor.value = value

    def stop(self):
        self.__set_value(0)

    def open(self):
        if self.current_status != "open":
            self.__set_value(self.OPEN_VALUE)
            time.sleep(self.RUN_TIME)
            self.stop()
            self.current_status = "open"

    def close(self):
        if self.current_status != "closed":
            self.__set_value(self.CLOSE_VALUE)
            time.sleep(self.RUN_TIME)
            self.stop()
            self.current_status = "closed"

    def schedule(self, T1, T2):
        raise NotImplementedError


if __name__ == "__main__":
    print("Try server.py")
