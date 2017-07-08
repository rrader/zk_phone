from time import sleep

from zk_phone.lib.io.keyboard import KeyboardInput
from zk_phone.lib.io.lcd_output import LCD
from zk_phone.lib.io.reed import ReedSwitchInput
from zk_phone.lib.net import get_ips


class StartState:
    def __init__(self, app):
        self.app = app
        self.app.lcd.print('HELLO', 0, 0)
        self.buf = None
        self.kb_clear_buf()

    def keypressed(self, event):
        self.buf.append(str(event.key))
        self.update_lcd()

        if self.kb_buffer_str == '*1#':
            for n, ip in enumerate(get_ips()[:2]):
                self.app.lcd.print(ip, pos_y=1, pos_x=0)
            self.kb_clear_buf()

    def kb_clear_buf(self):
        self.buf = []

    def update_lcd(self):
        self.app.lcd.clear()
        self.app.lcd.print(self.kb_buffer_str, 0, 0)

    @property
    def kb_buffer_str(self):
        return ''.join(self.buf)


class App:
    def __init__(self):
        self.kb = KeyboardInput(self.keypressed)
        self.reed = ReedSwitchInput(self.reed_switched)
        self.lcd = LCD()
        self.state = StartState(self)

    def keypressed(self, event):
        if hasattr(self.state, 'keypressed'):
            self.state.keypressed(event)

    def reed_switched(self, event):
        if hasattr(self.state, 'reed_switched'):
            self.state.reed_switched(event)

    def run(self):
        while True:
            sleep(1)


def create_app():
    return App()
