import keyboard
import mouse
from PyQt5 import QtWidgets


class Cat(QtWidgets.QWidget):
    def __init__(self):
        super(Cat, self).__init__()

    def update(self):
        pass

    def width(self):
        return 0

    @staticmethod
    def is_pressed(key):
        if "click" in key:
            key = key.split(" ")[0]
            return mouse.is_pressed(key)
        return keyboard.is_pressed(key)

