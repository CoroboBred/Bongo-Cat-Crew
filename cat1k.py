from PyQt5 import QtWidgets, QtGui  # import PyQt5 widgets


class Cat1k(QtWidgets.QWidget):
    key = {}
    textures = {}
    label = []
    layout = QtWidgets.QHBoxLayout()

    def __init__(self, key, textures):
        super(Cat1k, self).__init__()
        self.key = key
        self.textures = textures
        self.label = QtWidgets.QLabel("1k_cat")
        self.label.setPixmap(self.textures["0"])
        self.layout.addWidget(self.label)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def update_key(self, key, is_pressed):
        if self.key != key:
            return

        self.label.setPixmap(self.textures[str(int(is_pressed))])

