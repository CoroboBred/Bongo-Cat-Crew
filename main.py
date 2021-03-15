import sys

import keyboard
import win32gui
import win32process
import psutil
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets

import cat1k
import cat2k
import cat4k
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
            container = QtWidgets.QWidget()
            container.setLayout(layout)
            self.stack.addWidget(container)
            self.layout_indices[layout_key] = index
            self.cat_layouts[layout_key] = layout
            index = index + 1

        config = list(self.cat_configs.keys())[-1]  # get the last cat configuration.
        self.set_cat_layout(config)
        self.stack.setCurrentIndex(self.layout_indices["9"])
        self.setCentralWidget(self.stack)
        self.setStyleSheet("background-color: blue;")
        self.setWindowTitle("Bongo cat")

        # self.timer.timeout.connect(self.set_layout)
        # self.timer.start(2000)

        self.show()

    def set_cat_layout(self, config):
        layout = self.cat_layouts[config]
        if config not in self.cat_configs:
            return
        for cat in self.cat_configs[config]:
            layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

    def key_press(self, key, pressed):
        if "0" <= key <= "9":
            self.update_cats(key, pressed)
            return
        for cat in self.all_cats:
            self.all_cats[cat].update_key(key, pressed)

    def update_cats(self, key, pressed):
        if pressed or key not in self.layout_indices:
            return
        self.stack.setCurrentIndex(self.layout_indices[key])
        self.set_cat_layout(key)

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
        "2k": cat2k.Cat2k(cats_keys["2k"], textures["2k"]),
        "2k_rev": cat2k.Cat2k(cats_keys["2k_rev"], textures["2k_rev"]),
        "4k":    cat4k.Cat4k(cats_keys["4k"], textures["4k"]),
        "4k_rev": cat4k.Cat4k(cats_keys["4k_rev"], textures["4k_rev"]),
        "mk": cat2k.Cat2k(cats_keys["mk"], textures["2k"])
    }
    cat_configs = {
        "0": [cats["mk"]],
        "2": [cats["2k"]],
        "4": [cats["2k"], cats["2k_rev"]],
        "5": [cats["2k"], cats["1k"], cats["2k_rev"]],
        "9": [cats["4k"], cats["1k"], cats["4k_rev"]],
    }

    global win
    win = MainWindow(cat_configs, cats)
    emitter.key_updated.connect(win.key_press)

    keyboard.hook(key_event)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
