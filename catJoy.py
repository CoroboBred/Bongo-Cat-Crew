from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets

import cat


class CatJoy(cat.Cat):
    def __init__(self, keys, textures, timer):
        super(CatJoy, self).__init__()
        self.keys = keys
        self.textures = textures
        self.pressed_keys = [False for i in range(len(self.keys))]
        self.label = QtWidgets.QLabel("joystick_cat")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout = QtWidgets.QHBoxLayout()
        pix_map = self.textures["0000"].copy()
        self.w = pix_map.width()
        self.label.setPixmap(pix_map)
        self.layout.addWidget(self.label)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        timer.timeout.connect(self.update)

    def update(self):
        for i in range(len(self.keys)):
            self.pressed_keys[i] = self.is_pressed(self.keys[i])

        key = ""
        for k in self.pressed_keys:
            key += str(int(k))
        # If conflicting keys are pressed set the joystick to the neutral position.
        if (self.pressed_keys[0] and self.pressed_keys[2]) or (self.pressed_keys[1] and self.pressed_keys[3]):
            key = "0000"

        self.label.setPixmap(self.textures[key])

    def width(self):
        return self.w
