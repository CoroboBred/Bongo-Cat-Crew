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
    def __init__(self, cat_configs, all_cats):
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

        config = list(self.cat_configs.keys())[0]  # get the last cat configuration.
        self.set_cat_layout(config)
        self.stack.setCurrentIndex(self.layout_indices["0"])
        self.setCentralWidget(self.stack)
        self.setStyleSheet("background-color: blue;")
        self.setWindowTitle("Bongo cat")

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

    def key_press(self, key, pressed):
        if "0" <= key <= "9":
            self.update_cats(key, pressed)
            return
        for cat in self.all_cats:
            self.all_cats[cat].update_key(key, pressed)

    def update_cats(self, key, pressed=False):
        if pressed or key not in self.layout_indices:
            return
        self.stack.setCurrentIndex(self.layout_indices[key])

        if key not in self.cat_configs:
            return
        self.set_cat_layout(key)

    def set_cat_layout(self, key):
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


class Emitter(QtCore.QObject):
    key_updated = QtCore.pyqtSignal(str, bool)


win = {}
emitter = Emitter()


def key_event(e):
    key = e.name
    if key == "space":
        key = " "
    emitter.key_updated.emit(key, e.event_type == "down")


def main():
    app = QtWidgets.QApplication(sys.argv)

    cats_keys = read.read_config()
    textures = read.load_textures()
    cats = {
        "1k":   cat1k.Cat1k(cats_keys["1k"], textures["1k"]),
        "1k_tall":   cat1k.Cat1k(cats_keys["1k"], textures["1k_tall"]),
        "2k": cat2k.Cat2k(cats_keys["2k"], textures["2k"]),
        "2k_rev": cat2k.Cat2k(cats_keys["2k_rev"], textures["2k_rev"]),
        "4k":    cat4k.Cat4k(cats_keys["4k"], textures["4k"]),
        "4k_rev": cat4k.Cat4k(cats_keys["4k_rev"], textures["4k_rev"]),
        "mk": cat2k.Cat2k(cats_keys["mk"], textures["2k"]),
        "mc": catMouse.CatMouse(textures["mouse"]),
        "tc": catTalk.CatTalk(textures["talk"]),
    }
    cat_configs = {
        "0": [cats["mk"], cats["mc"], cats["tc"]],
        "1": [cats["1k"], cats["tc"]],
        "2": [cats["2k"], cats["tc"]],
        "4": [cats["2k"], cats["2k_rev"], cats["tc"]],
        "5": [cats["2k"], cats["1k"], cats["2k_rev"], cats["tc"]],
        "6": [cats["4k"], cats["4k_rev"], cats["tc"]],
        "7": [cats["4k"], cats["1k_tall"], cats["4k_rev"], cats["tc"]],
        "8": [cats["4k"], cats["4k_rev"], cats["tc"]],
        "9": [cats["4k"], cats["1k_tall"], cats["4k_rev"], cats["tc"]],
    }

    global win
    win = MainWindow(cat_configs, cats)
    emitter.key_updated.connect(win.key_press)

    keyboard.hook(key_event)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
