from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets
import sys
import keyboard
import cat4k
import cat1k
import read


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


def main():
    app = QtWidgets.QApplication(sys.argv)
    cats_keys = read.read_config()
    global win

    textures = read.load_textures()
    cats = [
        cat4k.Cat4k(cats_keys["4k_rev"], textures["4k_rev"]),
        cat1k.Cat1k(cats_keys["1k"], textures["1k"]),
        cat4k.Cat4k(cats_keys["4k"], textures["4k"]),
    ]
    win = MainWindow(cats)

    keyboard.hook(key_event)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
