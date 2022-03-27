# Author: Ryan Clifford
# 2022-03-26
import gpiozero
import os
class MotorController:
    def __init__(self, gpio_pin=17, min_pulse_width=0.001,
                 max_pulse_width=0.002, frame_width=0.020) -> None:
        os.system("pigpiod")
        gpiozero.Device.pin_factory = gpiozero.pins.pigpio.PiGPIOFactory
        self.motor = gpiozero.Servo(
            pin=gpio_pin, initial_value=0, min_pulse_width=min_pulse_width, 
            max_pulse_width=max_pulse_width, frame_width=frame_width)
    def Pin(self):
        return self.motor.pin
    def Value(self):
        return self.motor.value
    def set_value(self, value):
        self.motor.value = value


if __name__ == '__main__':
    print("Try server.py")