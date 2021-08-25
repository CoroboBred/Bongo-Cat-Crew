from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets

from cats import cat
import pyaudio
from array import array
from sys import byteorder
from random import randrange

THRESHOLD = 160
CHUNK_SIZE = 10000  # about .25 seconds.
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 44100
CHANNELS = 1
TRIM_APPEND = RATE / 4


class CatTalk(cat.Cat):
    def __init__(self, textures, timer):
        super(CatTalk, self).__init__()
        self.textures = textures
        self.is_talking = False
        self.index = 0
        self.trail = 0
        self.stale = 0
        self.label = QtWidgets.QLabel("talking_cat")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.indices = {}
        self.talking_textures = []
        for key, text in self.textures.items():
            if key == "idle":
                self.idle_texture = text
                self.label.setPixmap(text)
                continue
            self.talking_textures.append(text)

        self.w = self.idle_texture.width()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.thread = QtCore.QThread()
        self.listener = Listener()
        self.listener.moveToThread(self.thread)

        self.thread.started.connect(self.listener.listen)
        self.listener.talking_updater.connect(self.update_talking)
        self.thread.start()

        timer.timeout.connect(self.update)

    def update(self):
        if self.is_talking:
            self.label.setPixmap(self.talking_textures[self.index])
        else:
            self.label.setPixmap(self.idle_texture)

    def update_talking(self, talking):
        if not talking:
            if self.is_talking and self.trail <= 1:
                self.trail += 1
            else:
                self.trail = 0
                self.is_talking = False
            return

        self.trail = 0
        self.is_talking = True
        if self.stale == 3:
            self.stale = 0
            self.index = randrange(len(self.talking_textures))

        self.stale += 1

    def width(self):
        return self.w

class Listener(QtCore.QObject):
    talking_updater = QtCore.pyqtSignal(bool)

    def listen(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True,
                            frames_per_buffer=CHUNK_SIZE)

        prev_chunk = array('h', [])
        while True:
            # little endian, signed short
            data_chunk = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                data_chunk.byteswap()

            self.talking_updater.emit(is_talking(prev_chunk + data_chunk))
            prev_chunk = data_chunk


def is_talking(snd_data):
    # Returns 'True' if below the 'silent' threshold
    av = 0
    for i in range(len(snd_data)):
        if snd_data[i] > 0:
            av += snd_data[i]
    av /= len(snd_data)

    return av > THRESHOLD
