import datetime
from pad4pi import rpi_gpio


KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [4, 14, 15, 17]  # BCM numbering
COL_PINS = [18, 27, 22]  # BCM numbering

factory = rpi_gpio.KeypadFactory()


class KeyPressedEvent:
    def __init__(self, key):
        self.dt = datetime.datetime.now()
        self.key = key


class KeyboardInput:

    def __init__(self, callback):
        self.callback = callback
        self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
        self.attach()

    def attach(self):
        self.keypad.registerKeyPressHandler(self.handler)

    def handler(self, key):
        self.callback(KeyPressedEvent(key))
