import RPi.GPIO as GPIO
from charlcd import direct as lcd
from charlcd.drivers.gpio import Gpio


PINS = {
    'RS': 2,  # 0 ->instruction, 1->data
    'E': 3,
    'E2': None,
    'DB4': 4,
    'DB5': 14,
    'DB6': 15,
    'DB7': 18
}


class LCD:

    def __init__(self):
        gpio = Gpio()
        gpio.pins = PINS
        self._lcd = lcd.CharLCD(16, 2, gpio)
        self.attach()

    def attach(self):
        GPIO.setmode(GPIO.BCM)
        self._lcd.init()
        self._lcd.set_xy(0, 0)
        print('LCD attached')

    @property
    def lcd(self):
        return self._lcd

    def print(self, string, pos_x=None, pos_y=None):
        self.lcd.write(string, pos_x, pos_y)