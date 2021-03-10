from PyQt5 import QtWidgets, QtCore, QtGui  # import PyQt5 widgets
import sys
import os
import keyboard


class Cat(QtWidgets.QWidget):
    keys = []
    pressed_keys = []
    textures = {}
    l_label = []
    r_label = []
    layout = QtWidgets.QHBoxLayout()

    def __init__(self, keys):
        super(Cat, self).__init__()
        self.keys = keys
        self.pressed_keys = [False for i in range(len(self.keys))]
        self.load_textures()
        self.l_label= QtWidgets.QLabel("left")
        self.l_label.setPixmap(self.textures["l_00"])
        self.r_label = QtWidgets.QLabel("right")
        self.r_label.setPixmap(self.textures["r_00"])
        self.layout.addWidget(self.l_label)
        self.layout.addWidget(self.r_label)
        self.setLayout(self.layout)

    def load_textures(self):
        path = os.path.join(os.getcwd(), "images")
        l_00 = QtGui.QPixmap(os.path.join(path, "cat_l_00.png"))
        self.textures["l_00"] = l_00

        l_01 = QtGui.QPixmap(os.path.join(path, "cat_l_01.png"))
        self.textures["l_01"] = l_01

        l_10 = QtGui.QPixmap(os.path.join(path, "cat_l_10.png"))
        self.textures["l_10"] = l_10

        l_11 = QtGui.QPixmap(os.path.join(path, "cat_l_11.png"))
        self.textures["l_11"] = l_11

        r_00 = QtGui.QPixmap(os.path.join(path, "cat_r_00.png"))
        self.textures["r_00"] = r_00

        r_01 = QtGui.QPixmap(os.path.join(path, "cat_r_01.png"))
        self.textures["r_01"] = r_01

        r_10 = QtGui.QPixmap(os.path.join(path, "cat_r_10.png"))
        self.textures["r_10"] = r_10

        r_11 = QtGui.QPixmap(os.path.join(path, "cat_r_11.png"))
        self.textures["r_11"] = r_11

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
        self.l_label.setPixmap(l_text)
        self.r_label.setPixmap(r_text)


class MainWindow(QtWidgets.QMainWindow):
    cat = {}
    layout = QtWidgets.QHBoxLayout()

    def __init__(self, cat):
        super(MainWindow, self).__init__()
        self.cat = cat
        self.layout.addWidget(self.cat)
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("Bongo cat")
        self.show()

    def key_press(self, key, pressed):
        self.cat.update_key(key, pressed)
        self.layout.activate()


win = {}


def on_press(key):
    win.key_press(key, True)


def on_release(key):
    win.key_press(key, False)


def read_config():
    keys = []
    file = open("config.txt", "r")
    for line in file:
        split = line.split("=")
        if len(split) != 2:
            print("incorrectly formatted line: ", line)
            continue
        keys.append(split[1][0])
    file.close()

    return keys


def key_event(e):
    win.key_press(e.name, e.event_type == "down")


def main():
    app = QtWidgets.QApplication(sys.argv)
    keys = read_config()
    global win

    cat = Cat(keys)
    win = MainWindow(cat)

    keyboard.hook(key_event)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
