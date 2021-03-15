from PyQt5 import  QtGui  # import PyQt5 widgets
import os


def load_textures():
    path = os.path.join(os.getcwd(), "images")
    return {
        "1k": load_1k_textures(path),
        "2k": load_2k_textures(path),
        "2k_rev": load_rev_2k_textures(path),
        "4k": load_4k_textures(path),
        "4k_rev": load_rev_4k_textures(path),
    }


def load_1k_textures(path):
    path = os.path.join(path, "1k_cat")

    return {
        "0":  QtGui.QPixmap(os.path.join(path, "1k_cat_0.png")),
        "1":  QtGui.QPixmap(os.path.join(path, "1k_cat_1.png")),
    }


def load_2k_textures(path):
    path = os.path.join(path, "2k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "2k_cat_base.png")),
        "l_0": QtGui.QPixmap(os.path.join(path, "2k_cat_l_0.png")),
        "l_1": QtGui.QPixmap(os.path.join(path, "2k_cat_l_1.png")),
        "r_0": QtGui.QPixmap(os.path.join(path, "2k_cat_r_0.png")),
        "r_1": QtGui.QPixmap(os.path.join(path, "2k_cat_r_1.png")),
    }


def load_rev_2k_textures(path):
    path = os.path.join(path, "2k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "2k_cat_base.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "r_0": QtGui.QPixmap(os.path.join(path, "2k_cat_l_0.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "r_1": QtGui.QPixmap(os.path.join(path, "2k_cat_l_1.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "l_0": QtGui.QPixmap(os.path.join(path, "2k_cat_r_0.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "l_1": QtGui.QPixmap(os.path.join(path, "2k_cat_r_1.png")).transformed(QtGui.QTransform().scale(-1, 1)),
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


def load_rev_4k_textures(path):
    path = os.path.join(path, "4k_cat")
    return {
        "base": QtGui.QPixmap(os.path.join(path, "4k_cat_base.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "r_00": QtGui.QPixmap(os.path.join(path, "4k_cat_l_00.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "r_10": QtGui.QPixmap(os.path.join(path, "4k_cat_l_01.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "r_01": QtGui.QPixmap(os.path.join(path, "4k_cat_l_10.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "r_11": QtGui.QPixmap(os.path.join(path, "4k_cat_l_11.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "l_00": QtGui.QPixmap(os.path.join(path, "4k_cat_r_00.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "l_10": QtGui.QPixmap(os.path.join(path, "4k_cat_r_01.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "l_01": QtGui.QPixmap(os.path.join(path, "4k_cat_r_10.png")).transformed(QtGui.QTransform().scale(-1, 1)),
        "l_11": QtGui.QPixmap(os.path.join(path, "4k_cat_r_11.png")).transformed(QtGui.QTransform().scale(-1, 1)),
    }


def read_config():
    cats_keys = {}

    file = open("config.txt", "r")
    file.readline()  # read intro line and empty line
    file.readline()  # read blank line.

    file.readline()  # read 'Cat Layout' title.
    keys = []
    for i in range(9):
        keys.append(read_key(file.readline()))

    cats_keys["4k"] = keys[0:4]
    cats_keys["2k"] = keys[2:4]
    cats_keys["1k"] = keys[4]
    cats_keys["2k_rev"] = keys[5:7]
    cats_keys["4k_rev"] = keys[5:10]
    print(cats_keys)
    file.close()

    return cats_keys


def read_key(line):
    split = line.split("=")
    if len(split) != 2:
        raise str("incorrectly formatted line: ", line)
    return split[1][0]
