import os
import cv2
import dlib
from PyQt5 import QtWidgets, QtCore, QtGui  # import PyQt5 widgets

import cat
import pyaudio
from array import array
from sys import byteorder
from random import randrange
import numpy as np

THRESHOLD = 160
CHUNK_SIZE = 10000  # about .25 seconds.
FORMAT = pyaudio.paInt16
FRAME_MAX_VALUE = 2 ** 15 - 1
NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
RATE = 44100
CHANNELS = 1
TRIM_APPEND = RATE / 4


class CatTalkDynamic(cat.Cat):
    def __init__(self, textures, timer):
        super(CatTalkDynamic, self).__init__()
        self.textures = textures
        self.is_talking = False
        dlib.DLIB_USE_CUDA = True

        self.index = 0
        self.trail = 0
        self.stale = 0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.label = QtWidgets.QLabel("talking_dynamic_cat")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.indices = {}
        self.talking_textures = []
        for key, text in self.textures.items():
            if key == "base":
                self.base_texture = text
                self.label.setPixmap(text)
            elif key == "idle":
                self.idle_texture = text
            else:
                self.talking_textures.append(text)

        self.w = self.idle_texture.width()
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.talk_thread = QtCore.QThread()
        self.talk_listener = TalkListener()
        self.talk_listener.moveToThread(self.talk_thread)

        self.talk_thread.started.connect(self.talk_listener.listen)
        self.talk_listener.talking_updater.connect(self.update_talking)
        self.talk_thread.start()

        self.move_thread = QtCore.QThread()
        self.move_listener = MovementListener()
        self.move_listener.moveToThread(self.move_thread)

        self.move_thread.started.connect(self.move_listener.listen)
        self.move_listener.movement_updater.connect(self.update_movement)
        self.move_thread.start()

        timer.timeout.connect(self.update)

        self.frame = 0

    def update(self):
        self.frame += 1
        pix_map = self.base_texture.copy()
        painter = QtGui.QPainter(pix_map)
        if self.is_talking:
            painter.drawPixmap(self.offset_x, self.offset_y, self.talking_textures[self.index])
        else:
            painter.drawPixmap(self.offset_x, self.offset_y, self.idle_texture)
        painter.drawPixmap(0, 0, self.base_texture)
        painter.end()
        self.label.setPixmap(pix_map)

    def update_movement(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y

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


class MovementListener(QtCore.QObject):
    movement_updater = QtCore.pyqtSignal(float, float)

    def __init__(self):
        super(MovementListener, self).__init__()
        dat = os.path.join(os.getcwd(), "data", "shape_predictor_68_face_landmarks.dat")
        self.predictor = dlib.shape_predictor(dat)
        self.detector = dlib.get_frontal_face_detector()
        self.cap = cv2.VideoCapture(0)
        self.cap_width = self.cap.get(3)
        self.cap_height = self.cap.get(4)
        self.up = 0

    def listen(self):
        while True:
            ret, shape = self.shape()
            if not ret:
                continue
            self.up += 1
            center = shape[31]
            offset_x = center[0] / self.cap_width
            offset_x *= 100
            offset_x -= 75
            offset_y = center[1] / self.cap_height
            offset_y *= 100
            offset_y -= 75

            self.movement_updater.emit(offset_x, offset_y)

    def shape(self):
        ret, img = self.cap.read()
        if not ret:
            return False, None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        rects = self.detector(gray, 1)  # rects contains all the faces detected
        if len(rects) == 0:
            return False, None
        rect = rects[0]

        shape = self.predictor(gray, rect)
        shape = self.shape_to_np(shape)
        return True, shape

    @staticmethod
    def shape_to_np(shape, dtype="int"):
        coords = np.zeros((68, 2), dtype=dtype)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords


class TalkListener(QtCore.QObject):
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
