import keyboard
import mouse
import pygame
from PyQt5 import QtWidgets


class Cat(QtWidgets.QWidget):
    controller = None

    def __init__(self):
        super(Cat, self).__init__()
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            return
        controller = pygame.joystick.Joystick(0)
        controller.init()
        self.controller = controller

    def update(self):
        pass

    def width(self):
        return 0

    def is_pressed(self, key):
        if "click" in key:
            key = key.split(" ")[0]
            return mouse.is_pressed(key)
        elif "controller" in key:
            return self.is_controller_key_pressed(key)
        return keyboard.is_pressed(key)

    def is_controller_key_pressed(self, key):
        if self.controller is None:
            return False
        if "joystick" in key:
            return self.is_joystick_pressed(key)
        elif "hat" in key:
            return self.is_hat_pressed(key)
        return self.is_button_pressed(key)

    def is_joystick_pressed(self, key):
        pygame.event.get()  # User did something.

        # 'first' joystick.
        axis = 0
        if 'second' in key:  # 'second' joystick
            axis = 3

        # default is left/right. Vertical is always the next axis.
        if 'vertical' in key:
            axis += 1

        value = self.controller.get_axis(axis)
        if "left" in key or "up" in key:
            return value < -0.2
        else:  # right or down.
            return value > 0.2

    def is_hat_pressed(self, key):
        x, y = self.controller.get_hat(0)
        if "horizontal" in key:
            if "left" in key:
                return x == -1
            else:  # right
                return x == 1
        elif "vertical" in key:
            if "up" in key:
                return y == 1
            else:  # down
                return y == -1

    def is_button_pressed(self, key):
        return self.controller.get_button(int(key.split(" ")[2])) == 1
