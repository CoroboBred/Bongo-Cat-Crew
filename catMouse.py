from PyQt5 import QtWidgets, QtGui, QtCore  # import PyQt5 widgets

import cat
import pyautogui


class CatMouse(cat.Cat):
    def __init__(self, textures):
        super(CatMouse, self).__init__()
        self.textures = textures
        self.label = QtWidgets.QLabel("4k_cat")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.res_x, self.res_y = pyautogui.size()

        self.layout = QtWidgets.QHBoxLayout()
        pix_map = self.textures["base"]
        self.w = pix_map.width()
        self.h = pix_map.height()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.update_mouse()
        self.setLayout(self.layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_mouse)
        self.timer.start(10)

    def update_mouse(self):
        pix_map = self.textures["base"].copy()
        x, y = pyautogui.position()
        mouse_map = self.textures["mouse"].copy()
        mouse_map = mouse_map.scaled(int(self.w/2), int(self.h/2), QtCore.Qt.KeepAspectRatio)
        painter = QtGui.QPainter(pix_map)
        painter.drawPixmap(int((x/self.res_x * self.w)/1.5) + 160, int((y/self.res_y * self.h)/2)+70, mouse_map)
        painter.end()

        self.label.setPixmap(pix_map)
        self.layout.addWidget(self.label)

    def width(self):
        self.w
