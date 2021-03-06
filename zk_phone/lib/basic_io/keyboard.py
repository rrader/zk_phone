import datetime
from pad4pi import rpi_gpio

KEYPAD = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    ["*", 0, "#"]
]

ROW_PINS = [17, 24, 27, 23]  # BCM numbering
COL_PINS = [8, 22, 25]  # BCM numbering

factory = rpi_gpio.KeypadFactory()


class KeyPressedEvent:
    def __init__(self, key):
        self.dt = datetime.datetime.now()
        self.key = key


class KeyboardInput:

    def __init__(self, app, callback):
        self.app = app
        self.callback = callback
        self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

    def attach(self):
        self.keypad.registerKeyPressHandler(self.handler)
        print('Keypad attached')

    def handler(self, key):
        self.callback(KeyPressedEvent(key))
