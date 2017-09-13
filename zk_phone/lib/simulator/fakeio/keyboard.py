import datetime
from time import sleep

KEYPAD = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ["*", '0', "#"],
]


class KeyPressedEvent:
    def __init__(self, key):
        self.dt = datetime.datetime.now()
        self.key = key


class KeyboardInputSimulator:

    def __init__(self, app, callback):
        self.app = app
        self.callback = callback
        # self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

    def attach(self):
        for row in KEYPAD:
            for btn in row:
                self.app.canvas.tag_bind('btn' + btn, '<ButtonPress-1>', lambda event, btn=btn: self.handler(btn))
        print('Keypad attached')

    def handler(self, key):
        print(key)
        sleep(0.2)
        self.callback(KeyPressedEvent(key))
