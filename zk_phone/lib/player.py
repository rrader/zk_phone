import threading

import subprocess
from fcntl import fcntl, F_SETFL, F_GETFL
from os import read, O_NONBLOCK
from time import sleep


class Player(threading.Thread):
    def __init__(self, stream):
        self.stream = stream
        self.stdout = None
        self.stderr = None
        self.p = None
        self.terminated = False
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen(
            ["amixer", "cset", "numid=1", "100%"],
            shell=False
        )
        p.wait()
        self.p = subprocess.Popen(
            ["mplayer", "-playlist", self.stream],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1
        )

        flags = fcntl(self.p.stdout, F_GETFL)  # get current p.stdout flags
        fcntl(self.p.stdout, F_SETFL, flags | O_NONBLOCK)

        with self.p.stdout:
            while True:
                if self.terminated:
                    break

                try:
                    print(read(self.p.stdout.fileno(), 1024).decode())
                except OSError:
                    sleep(0.1)

    def kill(self):
        if self.p:
            self.p.kill()
            sleep(1)
            self.terminated = True


if __name__ == "__main__":
    a = Player("http://www.radioroks.ua/RadioROKS_32.m3u")
    a.start()
    sleep(10)
    a.kill()
