import sys

import keyboard
import win32gui
import win32process
import psutil
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets

import cat1k
import cat4k
import read


class MainWindow(QtWidgets.QMainWindow):
    all_cats = []
    cat_layouts = {}
    container = {}
    layer = {}
    timer = QtCore.QTimer()

    def __init__(self, cat_layouts, all_cats):
        super(MainWindow, self).__init__()

        self.cat_layouts = cat_layouts
        self.all_cats = all_cats

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for cat in self.cat_layouts["9k"]:
            self.layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.setStyleSheet("background-color: blue;")
        self.setWindowTitle("Bongo cat")

        self.timer.timeout.connect(self.set_layout)
        self.timer.start(2000)

        self.show()

    def key_press(self, key, pressed):
        for  cat in self.all_cats:
            self.all_cats[cat].update_key(key, pressed)
        self.layout.activate()

    def set_layout(self):
        window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(window)  # This produces a list of PIDs active window relates to
        name = psutil.Process(pid[-1]).name()  # pid[-1] is the most likely to survive last longer
        if name != "osu!.exe":
            return

        self.layout = QtWidgets.QHBoxLayout()
        config = self.get_config(win32gui.GetWindowText(window))
        for cat in self.cat_layouts[config]:
            self.layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.layout.activate()

    @staticmethod
    def get_config(title):
        if title.find("4k") != -1:
            return "4k"
        if title.find("5k") != -1:
            return "5k"
        if title.find("7k") != -1:
            return "9k"
        if title.find("9k") != -1:
            return "9k"
        return "4k"


win = {}


def key_event(e):
    key = e.name
    if key == "space":
        key = " "
    win.key_press(key, e.event_type == "down")


def main():
    app = QtWidgets.QApplication(sys.argv)

    cats_keys = read.read_config()
    textures = read.load_textures()
    cats = {
        "4k":    cat4k.Cat4k(cats_keys["4k_rev"], textures["4k_rev"]),
        "1k":   cat1k.Cat1k(cats_keys["1k"], textures["1k"]),
        "4k_rev": cat4k.Cat4k(cats_keys["4k"], textures["4k"]),
    }
    cat_layouts = {
        "4k": [cats["4k"]],
        "5k": [cats["4k"], cats["1k"]],
        "9k": [cats["4k"], cats["1k"], cats["4k_rev"]],
    }

    global win
    win = MainWindow(cat_layouts, cats)

    keyboard.hook(key_event)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
