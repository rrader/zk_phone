from pad4pi import rpi_gpio

from zk_phone.lib.events_queue.event import Event
from zk_phone.lib.events_queue.io import Input

KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [4, 14, 15, 17]  # BCM numbering
COL_PINS = [18, 27, 22]  # BCM numbering

factory = rpi_gpio.KeypadFactory()


class KeyboardInput(Input):

    def __init__(self, application):
        super().__init__(application)
        self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

    def attach(self):
        self.keypad.registerKeyPressHandler(self.handler)

    def handler(self, key):
        self.event(Event('keyboard', 'key_press', key=key))
