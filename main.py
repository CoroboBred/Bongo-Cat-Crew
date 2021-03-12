from PyQt5 import QtWidgets, QtGui , QtCore# import PyQt5 widgets
import sys
import os
import keyboard
import cat4k
import cat1k


class MainWindow(QtWidgets.QMainWindow):
    cats = []
    layout = QtWidgets.QHBoxLayout()

    def __init__(self, cats):
        super(MainWindow, self).__init__()
        self.cats = cats
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for cat in self.cats:
            self.layout.addWidget(cat, 0, QtCore.Qt.AlignBottom)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setStyleSheet("background-color: blue;")
        self.setWindowTitle("Bongo cat")
        self.show()

    def key_press(self, key, pressed):
        for cat in self.cats:
            cat.update_key(key, pressed)
        self.layout.activate()


win = {}


def key_event(e):
    key = e.name
    if key == "space":
        key = " "
    win.key_press(key, e.event_type == "down")


def load_textures():
    path = os.path.join(os.getcwd(), "images")
    return {
        "4k": load_4k_textures(path),
        "1k": load_1k_textures(path),
                }


def load_1k_textures(path):
    path = os.path.join(path, "1k_cat")

    return {
        "0":  QtGui.QPixmap(os.path.join(path, "1k_cat_0.png")),
        "1":  QtGui.QPixmap(os.path.join(path, "1k_cat_1.png")),
    }


def load_4k_textures(path):
    path = os.path.join(path, "4k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "4k_cat_base.png")),
        "l_00": QtGui.QPixmap(os.path.join(path, "4k_cat_l_00.png")),
        "l_01": QtGui.QPixmap(os.path.join(path, "4k_cat_l_01.png")),
        "l_10": QtGui.QPixmap(os.path.join(path, "4k_cat_l_10.png")),
        "l_11": QtGui.QPixmap(os.path.join(path, "4k_cat_l_11.png")),
        "r_00": QtGui.QPixmap(os.path.join(path, "4k_cat_r_00.png")),
        "r_01": QtGui.QPixmap(os.path.join(path, "4k_cat_r_01.png")),
        "r_10": QtGui.QPixmap(os.path.join(path, "4k_cat_r_10.png")),
        "r_11": QtGui.QPixmap(os.path.join(path, "4k_cat_r_11.png")),
    }


def read_config():
    cats_keys = {}

    file = open("config.txt", "r")
    file.readline()  # read intro line and empty line
    file.readline()

    file.readline()  # read 1-key title.
    key = read_key(file.readline())
    cats_keys["1k"] = key

    file.readline()  # read 4-key title.
    file.readline()
    keys = []
    for i in range(4):
        keys.append(read_key(file.readline()))
    cats_keys["4k"] = keys

    file.close()

    return cats_keys


def read_key(line):
    split = line.split("=")
    if len(split) != 2:
        raise str("incorrectly formatted line: ", line)
    return split[1][0]


def main():
    app = QtWidgets.QApplication(sys.argv)
    cats_keys = read_config()
    global win

    textures = load_textures()
    cats = {
        cat1k.Cat1k(cats_keys["1k"], textures["1k"]),
        cat4k.Cat4k(cats_keys["4k"], textures["4k"]),
    }
    win = MainWindow(cats)

    keyboard.hook(key_event)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
