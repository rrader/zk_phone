import datetime
from time import sleep


class ReedSwitchedEvent:
    def __init__(self, is_raised):
        self.dt = datetime.datetime.now()
        self.is_raised = is_raised


class ReedSwitchInputSimulator:
    def __init__(self, app, callback):
        self.app = app
        self.callback = callback
        self._is_raised = False

    def attach(self):
        self.app.canvas.tag_bind('handset', '<ButtonPress-1>', lambda event: self.handler())
        print('Reed switch attached ({})'.format(self.is_raised))

    def handler(self):
        self._is_raised = not self._is_raised
        if self._is_raised:
            self.app.canvas.move('handset', -100, 0)
        else:
            self.app.canvas.move('handset', 100, 0)
        self.app.canvas.update_idletasks()
        self.callback(ReedSwitchedEvent(self.is_raised))

    @property
    def is_raised(self):
        return self._is_raised
