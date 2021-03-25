from PyQt5 import QtGui  # import PyQt5 widgets
import os


def load_textures():
    path = os.path.join(os.getcwd(), "images")
    return {
        "1k": load_1k_textures(path, "", 252),
        "1k_tall": load_1k_textures(path, "_tall", 324),
        "2k": load_2k_textures(path),
        "2k_rev": load_rev_2k_textures(path),
        "4k": load_4k_textures(path),
        "4k_rev": load_rev_4k_textures(path),
        "mouse": load_mouse_textures(path),
        "talk": load_talking_textures(path),
        "joystick": load_joystick_textures(path),
        "button": load_button_textures(path),
    }


def load_joystick_textures(path):
    path = os.path.join(path, "joystick_cat")
    return {
        "0000": QtGui.QPixmap(os.path.join(path, "joystick_cat_idle.png")),
        "1000": QtGui.QPixmap(os.path.join(path, "joystick_cat_left.png")),
        "1100": QtGui.QPixmap(os.path.join(path, "joystick_cat_left_up.png")),
        "0100": QtGui.QPixmap(os.path.join(path, "joystick_cat_up.png")),
        "0110": QtGui.QPixmap(os.path.join(path, "joystick_cat_up_right.png")),
        "0010": QtGui.QPixmap(os.path.join(path, "joystick_cat_right.png")),
        "0011": QtGui.QPixmap(os.path.join(path, "joystick_cat_right_down.png")),
        "0001": QtGui.QPixmap(os.path.join(path, "joystick_cat_down.png")),
        "1001": QtGui.QPixmap(os.path.join(path, "joystick_cat_down_left.png")),
    }


def load_button_textures(path):
    path = os.path.join(path, "button_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "button_cat_base.png")),
        "l_00": QtGui.QPixmap(os.path.join(path, "button_cat_l_00.png")),
        "l_01": QtGui.QPixmap(os.path.join(path, "button_cat_l_01.png")),
        "l_10": QtGui.QPixmap(os.path.join(path, "button_cat_l_10.png")),
        "l_11": QtGui.QPixmap(os.path.join(path, "button_cat_l_11.png")),
        "r_00": QtGui.QPixmap(os.path.join(path, "button_cat_r_00.png")),
        "r_01": QtGui.QPixmap(os.path.join(path, "button_cat_r_01.png")),
        "r_10": QtGui.QPixmap(os.path.join(path, "button_cat_r_10.png")),
        "r_11": QtGui.QPixmap(os.path.join(path, "button_cat_r_11.png")),
    }


def load_talking_textures(path):
    path = os.path.join(path, "talking_cat")

    return {
        "idle":  QtGui.QPixmap(os.path.join(path, "cat_idle.png")),
        "talking_0":  QtGui.QPixmap(os.path.join(path, "cat_talking_0.png")),
        "talking_1":  QtGui.QPixmap(os.path.join(path, "cat_talking_1.png")),
        "talking_2": QtGui.QPixmap(os.path.join(path, "cat_talking_2.png")),
        "talking_3": QtGui.QPixmap(os.path.join(path, "cat_talking_3.png")),
        "talking_4": QtGui.QPixmap(os.path.join(path, "cat_talking_4.png")),
    }


def load_mouse_textures(path):
    path = os.path.join(path, "mouse_cat")

    return {
        "base":  QtGui.QPixmap(os.path.join(path, "mouse_cat_base.png")),
        "mouse":  QtGui.QPixmap(os.path.join(path, "mouse_cat_mouse.png")),
        "pad": QtGui.QPixmap(os.path.join(path, "mouse_cat_pad.png")),
    }


def load_1k_textures(path, mod, scale):
    path = os.path.join(path, "1k_cat")

    return {
        "0":  QtGui.QPixmap(os.path.join(path, "1k_cat" + mod + "_0.png")).scaledToWidth(scale),
        "1":  QtGui.QPixmap(os.path.join(path, "1k_cat" + mod + "_1.png")).scaledToWidth(scale),
    }


def load_2k_textures(path):
    path = os.path.join(path, "2k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "2k_cat_base.png")).scaledToWidth(231),
        "l_0": QtGui.QPixmap(os.path.join(path, "2k_cat_l_0.png")).scaledToWidth(231),
        "l_1": QtGui.QPixmap(os.path.join(path, "2k_cat_l_1.png")).scaledToWidth(231),
        "r_0": QtGui.QPixmap(os.path.join(path, "2k_cat_r_0.png")).scaledToWidth(231),
        "r_1": QtGui.QPixmap(os.path.join(path, "2k_cat_r_1.png")).scaledToWidth(231),
    }


def load_rev_2k_textures(path):
    path = os.path.join(path, "2k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "2k_cat_base.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
        "r_0": QtGui.QPixmap(os.path.join(path, "2k_cat_l_0.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
        "r_1": QtGui.QPixmap(os.path.join(path, "2k_cat_l_1.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
        "l_0": QtGui.QPixmap(os.path.join(path, "2k_cat_r_0.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
        "l_1": QtGui.QPixmap(os.path.join(path, "2k_cat_r_1.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
    }


def load_4k_textures(path):
    path = os.path.join(path, "4k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "4k_cat_base.png")).scaledToWidth(613),
        "l_00": QtGui.QPixmap(os.path.join(path, "4k_cat_l_00.png")).scaledToWidth(613),
        "l_01": QtGui.QPixmap(os.path.join(path, "4k_cat_l_01.png")).scaledToWidth(613),
        "l_10": QtGui.QPixmap(os.path.join(path, "4k_cat_l_10.png")).scaledToWidth(613),
        "l_11": QtGui.QPixmap(os.path.join(path, "4k_cat_l_11.png")).scaledToWidth(613),
        "r_00": QtGui.QPixmap(os.path.join(path, "4k_cat_r_00.png")).scaledToWidth(613),
        "r_01": QtGui.QPixmap(os.path.join(path, "4k_cat_r_01.png")).scaledToWidth(613),
        "r_10": QtGui.QPixmap(os.path.join(path, "4k_cat_r_10.png")).scaledToWidth(613),
        "r_11": QtGui.QPixmap(os.path.join(path, "4k_cat_r_11.png")).scaledToWidth(613),
    }


def load_rev_4k_textures(path):
    path = os.path.join(path, "4k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "4k_cat_base.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "r_00": QtGui.QPixmap(os.path.join(path, "4k_cat_l_00.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "r_10": QtGui.QPixmap(os.path.join(path, "4k_cat_l_01.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "r_01": QtGui.QPixmap(os.path.join(path, "4k_cat_l_10.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "r_11": QtGui.QPixmap(os.path.join(path, "4k_cat_l_11.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "l_00": QtGui.QPixmap(os.path.join(path, "4k_cat_r_00.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "l_10": QtGui.QPixmap(os.path.join(path, "4k_cat_r_01.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "l_01": QtGui.QPixmap(os.path.join(path, "4k_cat_r_10.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
        "l_11": QtGui.QPixmap(os.path.join(path, "4k_cat_r_11.png")).transformed(QtGui.QTransform().scale(-1, 1)).scaledToWidth(613),
    }


def read_config():
    cats_keys = {}

    file = open("config.txt", "r")
    file.readline()  # read intro line and empty line
    file.readline()  # read blank line.

    file.readline()  # read 'Mouse Layout' title.
    cats_keys["mk"] = [read_key(file.readline()), read_key(file.readline())]

    file.readline()  # read blank line.
    file.readline()  # read 'Mania Layout' title.
    keys = []
    for i in range(9):
        keys.append(read_key(file.readline()))

    cats_keys["4k"] = keys[0:4]
    cats_keys["2k"] = keys[2:4]
    cats_keys["1k"] = keys[4]
    cats_keys["2k_rev"] = keys[5:7]
    cats_keys["4k_rev"] = keys[5:10]
    cats_keys["3k"] = keys[3:6]

    file.readline()  # read blank line.
    file.readline()  # read 'Joystick Layout' line.
    joystick = []
    for i in range(10):
        joystick.append(read_key(file.readline()))
    cats_keys["bc"] = joystick[0:4]
    cats_keys["jc"] = joystick[4:8]
    cats_keys["lb"] = joystick[8]
    cats_keys["rb"] = joystick[9]

    file.close()

    return cats_keys


def read_key(line):
    split = line.split("=")
    if len(split) != 2:
        raise ValueError("incorrectly formatted line in config file: '" + line + "'")
    return split[1].strip()
