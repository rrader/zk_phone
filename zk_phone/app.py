from time import sleep

from zk_phone.lib.keyboard import KeyboardInput
from zk_phone.lib.lcd_output import LCD


class App:
    def __init__(self):
        self.kb = KeyboardInput(self.keypressed)
        self.lcd = LCD()

    def keypressed(self, event):
        print(event.key)

    def run(self):
        self.lcd.print('HELLO')
        while True:
            sleep(1)


def create_app():
    return App()
