from PyQt5 import QtWidgets, QtGui, QtCore  # import PyQt5 widgets

import cat

class Cat4k(cat.Cat):
    def __init__(self, keys, textures):
        super(Cat4k, self).__init__()
        self.keys = keys
        self.textures = textures
        self.pressed_keys = [False for i in range(len(self.keys))]
        self.label = QtWidgets.QLabel("4k_cat")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout = QtWidgets.QHBoxLayout()
        pix_map = self.textures["base"].copy()
        self.w = pix_map.width()
        painter = QtGui.QPainter(pix_map)
        painter.drawPixmap(0, 0, self.textures["l_00"])
        painter.drawPixmap(0, 0, self.textures["r_00"])
        painter.end()
        self.label.setPixmap(pix_map)
        self.layout.addWidget(self.label)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def update_key(self, key, is_pressed):
        index = -1
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                index = i
                break

        if index == -1:
            return

        self.pressed_keys[index] = is_pressed

        l_text = self.textures["l_" + str(int(self.pressed_keys[0])) + str(int(self.pressed_keys[1]))]
        r_text = self.textures["r_" + str(int(self.pressed_keys[2])) + str(int(self.pressed_keys[3]))]

        pix_map = self.textures["base"].copy()
        painter = QtGui.QPainter(pix_map)
        painter.drawPixmap(0, 0, l_text)
        painter.drawPixmap(0, 0, r_text)
        painter.end()
        self.label.setPixmap(pix_map)

    def width(self):
        return self.w
