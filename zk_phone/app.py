from time import sleep

from zk_phone.lib.net import get_ips
from zk_phone.lib.zakupki import zk_version


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


class NoState:
    def __init__(self, app):
        self.app = app


class HandsetPut(BaseState):
    def __init__(self, app, text='Hello!'):
        super().__init__(app)
        self.app.lcd.clear()
        self.app.lcd.print(text, 0, 0)
        self.buf = None
        self.kb_clear_buf()

    def keypressed(self, event):
        self.buf.append(str(event.key))
        self.update_lcd()

        if self.kb_buffer_str == '*1#':
            for n, ip in enumerate(get_ips()[:2]):
                self.app.lcd.print(ip, pos_y=1, pos_x=0)
            self.kb_clear_buf()

        if self.kb_buffer_str == '*7#':
            if zk_version():
                self.app.lcd.print(zk_version(), pos_y=1, pos_x=0)
            self.kb_clear_buf()

    def reed_switched(self, event):
        self.app.audio.speak("Hello. Type station number and hash")
        if event.is_raised:
            self.app.state = HandsetRaised(self.app)


class HandsetRaised(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.app.lcd.clear()
        self.app.lcd.print('Station and #', 0, 0)
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
        if station == 1:
            # Radio Rocks
            self.app.audio.play("http://www.radioroks.ua/RadioROKS.m3u")
        elif station == 2:
            # Lounge FM
            self.app.audio.play("http://cast.loungefm.com.ua:8000/loungefm.m3u")

    def reed_switched(self, event):
        self.app.audio.stop()
        if not event.is_raised:
            self.app.state = HandsetPut(self.app, 'Thank you!')


class App:
    def __init__(self):
        self.state = NoState(self)

        self.setup_io()

        self.reed.attach()
        self.lcd.attach()
        self.kb.attach()
        self.audio.attach()
        if self.reed.is_raised:
            self.state = HandsetRaised(self)
        else:
            self.state = HandsetPut(self)

    def setup_io(self):
        from zk_phone.lib.basic_io.keyboard import KeyboardInput
        from zk_phone.lib.basic_io.lcd_output import LCDOutput
        from zk_phone.lib.basic_io.reed import ReedSwitchInput
        from zk_phone.lib.player import AudioOutput
        from RPi import GPIO

        GPIO.setmode(GPIO.BCM)
        self.reed = ReedSwitchInput(self, self.reed_switched)
        self.lcd = LCDOutput(self)
        self.kb = KeyboardInput(self, self.keypressed)
        self.audio = AudioOutput(self)

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
