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
        self.eyes = [0, 0]
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
                self.idle_cat_texture = text
            elif key == "idle_eyes":
                self.idle_eyes_texture = text
            elif key == "talking_eyes":
                self.talking_eyes_texture = text
            else:
                self.talking_textures.append(text)

        self.w = self.idle_cat_texture.width()
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
        self.move_listener.movement_updater.connect(self.update_position)
        self.move_thread.start()

        timer.timeout.connect(self.update)

        self.frame = 0

    def update(self):
        self.frame += 1
        pix_map = self.base_texture.copy()
        painter = QtGui.QPainter(pix_map)
        if self.is_talking:
            painter.drawPixmap(self.offset_x, self.offset_y, self.talking_textures[self.index])
            painter.drawPixmap(self.offset_x + self.eyes[0], self.offset_y + self.eyes[1], self.talking_eyes_texture)
        else:
            painter.drawPixmap(self.offset_x, self.offset_y, self.idle_cat_texture)
            painter.drawPixmap(self.offset_x + self.eyes[0], self.offset_y + self.eyes[1], self.idle_eyes_texture)
        painter.drawPixmap(0, 0, self.base_texture)
        painter.end()
        self.label.setPixmap(pix_map)

    def update_position(self, position):
        self.update_movement(position[0])
        self.update_eyes(position[1])

    def update_eyes(self, eyes):
        self.eyes = eyes
        pass

    def update_movement(self, offset):
        self.offset_x = offset[0]
        self.offset_y = offset[1]

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
    movement_updater = QtCore.pyqtSignal(list)
    move_offset = [0, 0]
    pupils_offset = [[0, 0], [0, 0]]

    def __init__(self):
        super(MovementListener, self).__init__()
        dat = os.path.join(os.getcwd(), "data", "shape_predictor_68_face_landmarks.dat")
        self.predictor = dlib.shape_predictor(dat)
        self.detector = dlib.get_frontal_face_detector()
        self.cap = cv2.VideoCapture(0)
        self.cap_width = self.cap.get(3)
        self.cap_height = self.cap.get(4)
        self.up = 0
        self.kernel = np.ones((9, 9), np.uint8)

    def listen(self):
        while True:
            ret, img = self.cap.read()
            if not ret:
                return False, None

            ret, face = self.face(img)
            if not ret:
                continue
            self.up += 1
            self.move_offset = self.movement(face)
            ret, pupils_offset = self.pupils(img, face)
            if ret:
                self.pupils_offset = pupils_offset

            self.movement_updater.emit([self.move_offset, self.pupils_offset])

    def movement(self, face):
        center = face[30]
        offset_x = center[0] / self.cap_width
        offset_x *= 100
        offset_x -= 75
        offset_y = center[1] / self.cap_height
        offset_y *= 100
        offset_y -= 75
        return [offset_x, offset_y]

    def face(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        rects = self.detector(gray, 1)  # rects contains all the faces detected
        if len(rects) == 0:
            return False, None
        rect = rects[0]

        face = self.predictor(gray, rect)
        face = self.shape_to_np(face)
        return True, face

    def pupils(self, img, face):
        ret, pupils = self.find_pupils(img, face)
        if not ret:
            return False, None
        left = self.offset_pupils(face[36:42], pupils[0])
        right = self.offset_pupils(face[42:48], pupils[1])
        print("left: ", left, " right: ", right)
        # TODO: Fix offset calculation.
        return True, [(left[0] + right[0]) / 2, (left[1] + right[1]) / 2]

    @staticmethod
    def offset_pupils(eye, pupil):
        center = [0, 0]
        for point in eye:
            center[0] += point[0]
            center[1] += point[1]
        center[0] /= len(eye)
        center[1] /= len(eye)
        print("center: ", center)
        print("pupil: ", pupil)
        print("offset: ", [center[0] - pupil[0], center[1] - pupil[1]])

        return [center[0] - pupil[0], center[1] - pupil[1]]

    def find_pupils(self, img, face):
        left = [36, 37, 38, 39, 40, 41]  # keypoint indices for left eye
        right = [42, 43, 44, 45, 46, 47]  # keypoint indices for right eye
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        mask = self.eye_on_mask(face, mask, left)
        mask = self.eye_on_mask(face, mask, right)

        mask = cv2.dilate(mask, self.kernel, 5)
        eyes = cv2.bitwise_and(img, img, mask=mask)
        mask = (eyes == [0, 0, 0]).all(axis=2)
        eyes[mask] = [255, 255, 255]
        eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)

        threshold = 90  # optimal threshold for getting eye pupils. TODO turn into config argument.
        _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)
        thresh = cv2.medianBlur(thresh, 3)
        mid = (face[39][0] + face[42][0]) // 2
        pupils = [[0, 0], [0, 0]]
        ret, pupils[0][0], pupils[0][1] = self.contouring(thresh[:, 0:mid], mid)
        if not ret:
            return False, None
        ret, pupils[1][0], pupils[1][1] = self.contouring(thresh[:, mid:], mid, True)
        if not ret:
            return False, None

        return True, pupils

    @staticmethod
    def contouring(thresh, mid, right=False):
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        try:
            cnt = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            if right:
                cx += mid
            return True, cx, cy
        except:
            return False, 0, 0

    @staticmethod
    def shape_to_np(shape, dtype="int"):
        coords = np.zeros((68, 2), dtype=dtype)
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        return coords

    @staticmethod
    def eye_on_mask(face, mask, side):
        points = [face[i] for i in side]
        points = np.array(points, dtype=np.int32)
        mask = cv2.fillConvexPoly(mask, points, 255)
        return mask


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
