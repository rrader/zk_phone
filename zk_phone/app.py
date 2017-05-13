from zk_phone.controllers.keyboard_controller import KeyboardController
from zk_phone.io.keyboard_input import KeyboardInput
from zk_phone.io.lcd_output import LCDOutput
from zk_phone.lib.events_queue.application import App


def create_app():
    app = App()
    app.router.add_route('keyboard', KeyboardController)

    app.add_input('keyboard', KeyboardInput)
    app.add_output('lcd', LCDOutput)
    return app
