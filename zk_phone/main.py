import zk_phone.config
zk_phone.config.IS_SIMULATION_ENABLED = False

from zk_phone.app import create_app


app = create_app()


def main():
    app.run()
