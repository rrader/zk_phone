import datetime

from RPi import GPIO

REED_SWITCH = 7  # BCM numbering


class ReedSwitchedEvent:
    def __init__(self, is_raised):
        self.dt = datetime.datetime.now()
        self.is_raised = is_raised


class ReedSwitchInput:

    def __init__(self, app, callback):
        self.app = app
        self.callback = callback
        GPIO.setup(REED_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def attach(self):
        GPIO.add_event_detect(REED_SWITCH, GPIO.BOTH, callback=self.handler, bouncetime=300)
        print('Reed switch attached ({})'.format(self.is_raised))

    def handler(self, channel):
        self.callback(ReedSwitchedEvent(self.is_raised))

    @property
    def is_raised(self):
        return not GPIO.input(REED_SWITCH)
