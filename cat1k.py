from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets


class Cat1k(QtWidgets.QWidget):
    def __init__(self, key, textures):
        super(Cat1k, self).__init__()
        self.key = key
        self.textures = textures
        self.label = QtWidgets.QLabel("1k_cat")
        text = self.textures["0"]
        self.w = text.width()
        self.label.setPixmap(text)
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def update_key(self, key, is_pressed):
        if self.key != key:
            return

        self.label.setPixmap(self.textures[str(int(is_pressed))])

    def width(self):
        return self.w

