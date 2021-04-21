from PyQt5 import QtWidgets, QtGui, QtCore  # import PyQt5 widgets

import cat


class CatBoard(cat.Cat):
    def __init__(self, keys, text_4k, text_4k_rev, timer):
        super(CatBoard, self).__init__()
        self.layout = QtWidgets.QHBoxLayout()
        self.cats = []
        self.w = 0
        for i in range(0, 12, 4):
            text = text_4k_rev
            if i % 8 == 0:
                text = text_4k

            cat_keys = []
            for j in range(4):
                keys_up = keys["kb_" + str(j) + '0']
                keys_down = keys["kb_" + str(j) + '1']
                cat_keys.append(keys_up[i:i + 4])
                cat_keys.append(keys_down[i:i + 4])
            c = Cat4k(cat_keys, text, timer)
            self.w += c.width()
            self.cats.append(c)
            self.layout.addWidget(c)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def update(self):
        pass

    def width(self):
        return self.w


class Cat4k(cat.Cat):
    def __init__(self, keys, textures, timer):
        super(Cat4k, self).__init__()
        self.keys = keys
        self.textures = textures
        self.pressed_keys = [False for i in range(len(self.keys[0]))]
        self.label = QtWidgets.QLabel("4k_board_cat")
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
        timer.timeout.connect(self.update)

    def update(self):
        for i in range(len(self.keys[0])):
            is_pressed = False
            for row in self.keys:
                if self.is_pressed(row[i]):
                    is_pressed = True
                    break
            self.pressed_keys[i] = is_pressed

        l_text = self.textures["l_" + str(int(self.pressed_keys[0])) + str(int(self.pressed_keys[1]))]
        r_text = self.textures["r_" + str(int(self.pressed_keys[2])) + str(int(self.pressed_keys[3]))]

        pix_map = self.textures["base"].copy()
        painter = QtGui.QPainter(pix_map)
        # Draw the right side first so that it will overlay on top of the left side.
        painter.drawPixmap(0, 0, r_text)
        painter.drawPixmap(0, 0, l_text)
        painter.end()
        self.label.setPixmap(pix_map)

    def width(self):
        return self.w
