from time import sleep

from zk_phone.lib.keyboard import KeyboardInput


class App:
    def __init__(self):
        self.kb = KeyboardInput(self.keypressed)

    def keypressed(self, event):
        print(event.key)

    def run(self):
        while True:
            sleep(1)


def create_app():
    return App()
