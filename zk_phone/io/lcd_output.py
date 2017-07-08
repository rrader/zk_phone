import RPi.GPIO as GPIO
from charlcd import direct as lcd
from charlcd.drivers.gpio import Gpio

from zk_phone.lib.events_queue.io import Output

PINS = {
    'RS': 2,  # 0 ->instruction, 1->data
    'E': 3,
    'E2': None,
    'DB4': 4,
    'DB5': 14,
    'DB6': 15,
    'DB7': 18
}


class LCDOutput(Output):

    def __init__(self, application):
        super().__init__(application)
        gpio = Gpio()
        gpio.pins = PINS
        self._lcd = lcd.CharLCD(16, 2, gpio)

    def attach(self):
        GPIO.setmode(GPIO.BCM)
        self._lcd.init()
        self._lcd.set_xy(0, 0)

    @property
    def lcd(self):
        return self._lcd
