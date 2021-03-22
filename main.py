import sys

import keyboard
import win32gui
import win32process
import psutil
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets

import cat1k
import cat2k
import cat4k
import catMouse
import catTalk
import read


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, cat_configs, all_cats, timer):
        super(MainWindow, self).__init__()

        self.cat_configs = cat_configs
        self.all_cats = all_cats

        self.stack = QtWidgets.QStackedWidget()
        self.layout_indices = {}
        self.cat_layouts = {}
        index = 0
        for layout_key in self.cat_configs:
            layout = QtWidgets.QHBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
            container = QtWidgets.QWidget()
            container.setLayout(layout)
            self.stack.addWidget(container)
            self.layout_indices[layout_key] = index
            self.cat_layouts[layout_key] = layout
            index = index + 1

        key = list(self.cat_configs.keys())[0]  # get the first cat configuration.
        self.set_cat_layout(key)
        self.setCentralWidget(self.stack)
        self.setStyleSheet("background-color: blue;")
        self.setWindowTitle("Bongo cat")
        self.keys = [chr(c) for c in range(48, 58)]

        timer.timeout.connect(self.update)
        self.show()

    def set_width(self):
        max_width = 0
        for key in self.cat_configs:
            width = 0
            for cat in self.cat_configs[key]:
                width = width + cat.width()
            if width > max_width:
                max_width = width
        self.setFixedWidth(max_width)

    def update(self):
        for key in self.keys:
            if keyboard.is_pressed(key):
                self.set_cat_layout(key)

    def set_cat_layout(self, key):
        self.stack.setCurrentIndex(self.layout_indices[key])

        layout = self.cat_layouts[key]
        buffer = QtWidgets.QWidget()
        buffer.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        layout.addWidget(buffer)
        for cat in self.cat_configs[key]:
            layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

    # TODO: Update 'set_layout func to read and render osu! title instead.
#   def set_layout(self):
#       window = win32gui.GetForegroundWindow()
#       pid = win32process.GetWindowThreadProcessId(window)  # This produces a list of PIDs active window relates to
#       name = psutil.Process(pid[-1]).name()  # pid[-1] is the most likely to survive last longer
#       if name != "osu!.exe":
#           return

#       self.layout = QtWidgets.QHBoxLayout()
#       config = self.get_config(win32gui.GetWindowText(window))
#       for cat in self.cat_layouts[config]:
#           self.layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)
#       self.container = QtWidgets.QWidget()
#       self.container.setLayout(self.layout)
#       self.setCentralWidget(self.container)

#       self.layout.activate()


win = {}


def main():
    app = QtWidgets.QApplication(sys.argv)

    cats_keys = read.read_config()
    textures = read.load_textures()
    timer = QtCore.QTimer()
    cats = {
        "1k":   cat1k.Cat1k(cats_keys["1k"], textures["1k"], timer),
        "1k_tall":   cat1k.Cat1k(cats_keys["1k"], textures["1k_tall"], timer),
        "2k": cat2k.Cat2k(cats_keys["2k"], textures["2k"], timer),
        "2k_rev": cat2k.Cat2k(cats_keys["2k_rev"], textures["2k_rev"], timer),
        "4k":    cat4k.Cat4k(cats_keys["4k"], textures["4k"], timer),
        "4k_rev": cat4k.Cat4k(cats_keys["4k_rev"], textures["4k_rev"], timer),
        "mk": cat2k.Cat2k(cats_keys["mk"], textures["2k"], timer),
        "mc": catMouse.CatMouse(textures["mouse"], timer),
        "tc": catTalk.CatTalk(textures["talk"], timer),
    }
    cat_configs = {
        "0": [cats["mk"], cats["mc"], cats["tc"]],
        "1": [cats["1k"]],
        "2": [cats["2k"]],
        "4": [cats["2k"], cats["2k_rev"] ],
        "5": [cats["2k"], cats["1k"], cats["2k_rev"]],
        "6": [cats["4k"], cats["4k_rev"]],
        "7": [cats["4k"], cats["1k_tall"], cats["4k_rev"]],
        "8": [cats["4k"], cats["4k_rev"]],
        "9": [cats["4k"], cats["1k_tall"], cats["4k_rev"]],
        "-": [cats["tc"]],
    }

    global win
    win = MainWindow(cat_configs, cats, timer)
    timer.start(int(100 / 4))  # 40 fps

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
