import threading

import subprocess
from fcntl import fcntl, F_SETFL, F_GETFL
from os import read, O_NONBLOCK
from time import sleep


class Player(threading.Thread):
    def __init__(self, audio, stream):
        self.audio = audio
        self.stream = stream
        self.stdout = None
        self.stderr = None
        self.p = None
        self.terminated = False
        threading.Thread.__init__(self)

    def run(self):
        self.audio.audio_max()
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


class Speak(threading.Thread):
    def __init__(self, audio, text):
        self.audio = audio
        self.text = text
        self.stdout = None
        self.stderr = None
        self.p = None
        self.terminated = False
        threading.Thread.__init__(self)

    def run(self):
        self.audio.audio_max()
        self.p = subprocess.Popen(
            ['echo "{}" | festival --tts'.format(self.text)],
            shell=True,
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
                    read(self.p.stdout.fileno(), 1024).decode()
                except OSError:
                    sleep(0.1)

    def kill(self):
        if self.p:
            self.p.kill()
            sleep(1)
            self.terminated = True


class AudioOutput:
    def __init__(self, app):
        self.app = app
        self._player = None
        self._speak = None

    def attach(self):
        self.audio_min()

    def audio_max(self):
        p = subprocess.Popen(
            ["amixer", "cset", "numid=1", "100%"],
            shell=False
        )
        p.wait()

    def audio_min(self):
        p = subprocess.Popen(
            ["amixer", "cset", "numid=1", "0%"],
            shell=False
        )
        p.wait()

    def play(self, file):
        self.stop()
        self._player = Player(self, file)
        self._player.start()

    def speak(self, text):
        self.stop()
        self._speak = Speak(self, text)
        self._speak.start()

    def stop(self):
        if self._player:
            self._player.kill()
        if self._speak:
            self._speak.kill()


if __name__ == "__main__":
    a = Player("http://www.radioroks.ua/RadioROKS_32.m3u")
    a.start()
    sleep(10)
    a.kill()
