from time import sleep

from zk_phone.lib.io.keyboard import KeyboardInput
from zk_phone.lib.io.lcd_output import LCD
from zk_phone.lib.io.reed import ReedSwitchInput
from zk_phone.lib.net import get_ips


class BaseState:
    def __init__(self, app):
        self.app = app

    def kb_clear_buf(self):
        self.buf = []

    def update_lcd(self):
        if len(self.kb_buffer_str) <= 1:
            self.app.lcd.clear([0])
        self.app.lcd.print(self.kb_buffer_str, 0, 0)

    @property
    def kb_buffer_str(self):
        return ''.join(self.buf)


class HandsetPut(BaseState):
    def __init__(self, app):
        super().__init__(app)
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

    def reed_switched(self, event):
        if event.is_raised:
            self.app.state = HandsetRaised(self.app)


class HandsetRaised(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.app.lcd.print('Station number and #', 0, 0)
        self.buf = None
        self.kb_clear_buf()

    def keypressed(self, event):
        self.buf.append(str(event.key))
        self.update_lcd()

        if self.kb_buffer_str[-1] == '#':
            self.play()
            self.kb_clear_buf()

    def play(self):
        station = int(self.kb_buffer_str[:-1])
        self.app.lcd.print('Playing {}'.format(station), pos_y=1, pos_x=0)

    def reed_switched(self, event):
        if not event.is_raised:
            self.app.state = HandsetPut(self.app)


class App:
    def __init__(self):
        self.reed = ReedSwitchInput(self.reed_switched)
        self.lcd = LCD()
        self.kb = KeyboardInput(self.keypressed)

        self.reed.attach()
        if self.reed.is_raised:
            self.state = HandsetRaised(self)
        else:
            self.state = HandsetPut(self)

        self.lcd.attach()
        self.kb.attach()

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
