from PyQt5 import QtWidgets, QtGui, QtCore  # import PyQt5 widgets

import cat
import pyaudio
from array import array
from sys import byteorder
from random import randrange

THRESHOLD = 100
CHUNK_SIZE = 10000  # about .25 seconds.
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 44100
CHANNELS = 1
TRIM_APPEND = RATE / 4


class CatTalk(cat.Cat):
    def __init__(self, textures):
        super(CatTalk, self).__init__()
        self.textures = textures
        self.is_talking = False
        self.index = 0
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

    def update_talking(self, talking):
        if not talking:
            self.label.setPixmap(self.idle_texture)
            return

        index = self.index
        if self.stale == 3:
            self.stale = 0
            index = randrange(len(self.talking_textures))

        self.label.setPixmap(self.talking_textures[index])
        self.stale += 1


class Listener(QtCore.QObject):
    talking_updater = QtCore.pyqtSignal(bool)

    def listen(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True,
                            frames_per_buffer=CHUNK_SIZE)

        while True:
            # little endian, signed short
            data_chunk = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                data_chunk.byteswap()

            self.talking_updater.emit(is_talking(data_chunk))


def is_talking(snd_data):
    # Returns 'True' if below the 'silent' threshold
    av = 0
    for i in range(len(snd_data)):
        if snd_data[i] > 0:
            av += snd_data[i]
    av /= len(snd_data)

    return av > THRESHOLD
