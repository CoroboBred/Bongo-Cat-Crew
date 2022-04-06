import os
import json

import pygame
from PyQt5 import QtCore, QtGui  # import PyQt5 widgets

from cats import cat4k, cat1k, catJoy, catBoard, catTalk, cat2k, catMouse


class Config:
    textures = {}
    keys = {}
    default_layout = '-'
    icon = {}
    enable_dynamic_layout = True
    enable_talking = True
    enable_bumpers = False
    enable_dynamic_talking = False
    mouse_type = "mouse_game"
    fps = 40

    def __init__(self):
        self.load_textures()
        self.load_config()
        self.load_key_layout()
        self.timer = QtCore.QTimer()
        cats = {
            "1k": cat1k.Cat1k(self.keys["1k"], self.textures["1k"], self.timer),
            "1k_m": cat1k.Cat1k(self.keys["1k"], self.textures["1k"], self.timer),
            "1k_tall": cat1k.Cat1k(self.keys["1k"], self.textures["1k_tall"], self.timer),
            "1k_l": cat1k.Cat1k(self.keys["3k"][0], self.textures["1k"], self.timer),
            "1k_r": cat1k.Cat1k(self.keys["3k"][2], self.textures["1k"], self.timer),
            "2k": cat2k.Cat2k(self.keys["2k"], self.textures["2k"], self.timer),
            "2k_4": cat2k.Cat2k(self.keys["2k"], self.textures["2k"], self.timer),
            "2k_5": cat2k.Cat2k(self.keys["2k"], self.textures["2k"], self.timer),
            "2k_rev_4": cat2k.Cat2k(self.keys["2k_rev"], self.textures["2k_rev"], self.timer),
            "2k_rev_5": cat2k.Cat2k(self.keys["2k_rev"], self.textures["2k_rev"], self.timer),
            "4k_6": cat4k.Cat4k(self.keys["4k"], self.textures["4k"], self.timer),
            "4k_7": cat4k.Cat4k(self.keys["4k"], self.textures["4k"], self.timer),
            "4k_8": cat4k.Cat4k(self.keys["4k"], self.textures["4k"], self.timer),
            "4k_9": cat4k.Cat4k(self.keys["4k"], self.textures["4k"], self.timer),
            "4k_rev_6": cat4k.Cat4k(self.keys["4k_rev"], self.textures["4k_rev"], self.timer),
            "4k_rev_7": cat4k.Cat4k(self.keys["4k_rev"], self.textures["4k_rev"], self.timer),
            "4k_rev_8": cat4k.Cat4k(self.keys["4k_rev"], self.textures["4k_rev"], self.timer),
            "4k_rev_9": cat4k.Cat4k(self.keys["4k_rev"], self.textures["4k_rev"], self.timer),
            "mkg": cat2k.Cat2k(self.keys["mkg"], self.textures["2k"], self.timer),
            "mko": cat2k.Cat2k(self.keys["mko"], self.textures["2k"], self.timer),
            "mc": catMouse.CatMouse(self.textures["mouse"], self.timer),
            "mjg": catJoy.CatJoy(self.keys["mjg"], self.textures["joystick"], self.timer),
            "tc": catTalk.CatTalk(self.textures["talk"], self.timer, self.enable_dynamic_talking),
            "bc": cat4k.Cat4k(self.keys["bc"], self.textures["button"], self.timer),
            "jc": catJoy.CatJoy(self.keys["jc"], self.textures["joystick"], self.timer),
            "lb": cat1k.Cat1k(self.keys["lb"], self.textures["1k"], self.timer),
            "rb": cat1k.Cat1k(self.keys["rb"], self.textures["1k"], self.timer),
            "kb": catBoard.CatBoard(self.keys["kb"], self.textures["4k"], self.textures["4k_rev"], self.timer),
            "stadia_lb": cat1k.Cat1k(self.keys["stadia_lb"], self.textures["1k"], self.timer),
            "stadia_hat": cat4k.Cat4k(self.keys["stadia_hat"], self.textures["button"], self.timer),
            "stadia_jc_1": catJoy.CatJoy(self.keys["stadia_jc_1"], self.textures["joystick_rev"], self.timer),
            "stadia_jc_2": catJoy.CatJoy(self.keys["stadia_jc_2"], self.textures["joystick"], self.timer),
            "stadia_bc": cat4k.Cat4k(self.keys["stadia_bc"], self.textures["button_rev"], self.timer),
            "stadia_rb": cat1k.Cat1k(self.keys["stadia_rb"], self.textures["1k"], self.timer),

        }

        self.all_layouts = {
            "0": [],
            "1": [cats["1k"]],
            "2": [cats["2k"]],
            "3": [cats["1k_l"], cats["1k_m"], cats["1k_r"]],
            "4": [cats["2k_4"], cats["2k_rev_4"]],
            "5": [cats["2k_5"], cats["1k"], cats["2k_rev_5"]],
            "6": [cats["4k_6"], cats["4k_rev_6"]],
            "7": [cats["4k_7"], cats["1k_tall"], cats["4k_rev_7"]],
            "8": [cats["4k_8"], cats["4k_rev_8"]],
            "9": [cats["4k_9"], cats["1k_tall"], cats["4k_rev_9"]],
            "=": [cats["kb"]]
        }

        if self.mouse_type == "mouse_osu":
            self.all_layouts["-"] = [cats["mko"], cats["mc"]]
        else:  # default to mouse_game type.
            self.all_layouts["-"] = [cats["mkg"], cats["mjg"], cats["mc"]]

        if self.enable_bumpers:
            self.all_layouts["`"] = [cats["lb"], cats["bc"], cats["rb"], cats["jc"]]
            self.all_layouts["backspace"] = [cats["stadia_lb"], cats["stadia_hat"], cats["stadia_jc_1"], cats["stadia_jc_2"],
                                     cats["stadia_bc"], cats["stadia_rb"]]
        else:
            self.all_layouts["`"] = [cats["bc"], cats["jc"]]
            self.all_layouts["backspace"] = [cats["stadia_hat"], cats["stadia_jc_1"], cats["stadia_jc_2"], cats["stadia_bc"]]

        if self.enable_talking:
            for layout in self.all_layouts.values():
                layout.append(cats["tc"])

        if self.enable_dynamic_layout:
            self.layouts = self.all_layouts
        else:
            self.layouts = {self.default_layout: self.all_layouts[self.default_layout]}

    def load_textures(self):
        path = os.path.join(os.getcwd(), "images")
        self.textures = {
            "1k": self.load_1k_textures(path, "", 252),
            "1k_tall": self.load_1k_textures(path, "_tall", 500),
            "2k": self.load_2k_textures(path),
            "2k_rev": self.load_rev_2k_textures(path),
            "4k": self.load_4k_textures(path),
            "4k_rev": self.load_rev_4k_textures(path),
            "mouse": self.load_mouse_textures(path),
            "talk": self.load_talking_textures(path),
            "talk": self.load_talking_textures(path),
            "joystick": self.load_joystick_textures(path),
            "joystick_rev": self.load_rev_joystick_textures(path),
            "button": self.load_button_textures(path),
            "button_rev": self.load_rev_button_textures(path),
        }
        self.icon = QtGui.QIcon(os.path.join(path, "icon.png"))

    @staticmethod
    def load_joystick_textures(path):
        path = os.path.join(path, "joystick_cat")
        return {
            "0000": QtGui.QPixmap(os.path.join(path, "joystick_cat_idle.png")).scaledToWidth(250),
            "1000": QtGui.QPixmap(os.path.join(path, "joystick_cat_left.png")).scaledToWidth(250),
            "1100": QtGui.QPixmap(os.path.join(path, "joystick_cat_left_up.png")).scaledToWidth(250),
            "0100": QtGui.QPixmap(os.path.join(path, "joystick_cat_up.png")).scaledToWidth(250),
            "0110": QtGui.QPixmap(os.path.join(path, "joystick_cat_up_right.png")).scaledToWidth(250),
            "0010": QtGui.QPixmap(os.path.join(path, "joystick_cat_right.png")).scaledToWidth(250),
            "0011": QtGui.QPixmap(os.path.join(path, "joystick_cat_right_down.png")).scaledToWidth(250),
            "0001": QtGui.QPixmap(os.path.join(path, "joystick_cat_down.png")).scaledToWidth(250),
            "1001": QtGui.QPixmap(os.path.join(path, "joystick_cat_down_left.png")).scaledToWidth(250),
        }

    @staticmethod
    def load_rev_joystick_textures(path):
        path = os.path.join(path, "joystick_cat")
        return {
            "0000": QtGui.QPixmap(os.path.join(path, "joystick_cat_idle.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "0010": QtGui.QPixmap(os.path.join(path, "joystick_cat_left.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "0110": QtGui.QPixmap(os.path.join(path, "joystick_cat_left_up.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "0100": QtGui.QPixmap(os.path.join(path, "joystick_cat_up.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "1100": QtGui.QPixmap(os.path.join(path, "joystick_cat_up_right.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "1000": QtGui.QPixmap(os.path.join(path, "joystick_cat_right.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "1001": QtGui.QPixmap(os.path.join(path, "joystick_cat_right_down.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "0001": QtGui.QPixmap(os.path.join(path, "joystick_cat_down.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
            "0011": QtGui.QPixmap(os.path.join(path, "joystick_cat_down_left.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(250),
        }

    @staticmethod
    def load_button_textures(path):
        path = os.path.join(path, "button_cat")
        return {
            "base": QtGui.QPixmap(os.path.join(path, "button_cat_base.png")).scaledToWidth(325),
            "l_00": QtGui.QPixmap(os.path.join(path, "button_cat_l_00.png")).scaledToWidth(325),
            "l_01": QtGui.QPixmap(os.path.join(path, "button_cat_l_01.png")).scaledToWidth(325),
            "l_10": QtGui.QPixmap(os.path.join(path, "button_cat_l_10.png")).scaledToWidth(325),
            "l_11": QtGui.QPixmap(os.path.join(path, "button_cat_l_11.png")).scaledToWidth(325),
            "r_00": QtGui.QPixmap(os.path.join(path, "button_cat_r_00.png")).scaledToWidth(325),
            "r_01": QtGui.QPixmap(os.path.join(path, "button_cat_r_01.png")).scaledToWidth(325),
            "r_10": QtGui.QPixmap(os.path.join(path, "button_cat_r_10.png")).scaledToWidth(325),
            "r_11": QtGui.QPixmap(os.path.join(path, "button_cat_r_11.png")).scaledToWidth(325),
        }

    @staticmethod
    def load_rev_button_textures(path):
        path = os.path.join(path, "button_cat")
        return {
            "base": QtGui.QPixmap(os.path.join(path, "button_cat_base.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "l_00": QtGui.QPixmap(os.path.join(path, "button_cat_r_00.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "l_01": QtGui.QPixmap(os.path.join(path, "button_cat_r_10.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "l_10": QtGui.QPixmap(os.path.join(path, "button_cat_r_01.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "l_11": QtGui.QPixmap(os.path.join(path, "button_cat_r_11.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "r_00": QtGui.QPixmap(os.path.join(path, "button_cat_l_00.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "r_01": QtGui.QPixmap(os.path.join(path, "button_cat_l_10.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "r_10": QtGui.QPixmap(os.path.join(path, "button_cat_l_01.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
            "r_11": QtGui.QPixmap(os.path.join(path, "button_cat_l_11.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(325),
        }

    @staticmethod
    def load_talking_textures(path):
        path = os.path.join(path, "talking_cat")

        return {
            "idle": QtGui.QPixmap(os.path.join(path, "dynamic_idle.png")),
            "idle_eyes": QtGui.QPixmap(os.path.join(path, "dynamic_idle_eyes.png")),
            "base": QtGui.QPixmap(os.path.join(path, "dynamic_talking_base.png")),
            "talking_0": QtGui.QPixmap(os.path.join(path, "dynamic_talking_0.png")),
            "talking_1": QtGui.QPixmap(os.path.join(path, "dynamic_talking_1.png")),
            "talking_2": QtGui.QPixmap(os.path.join(path, "dynamic_talking_2.png")),
            "talking_3": QtGui.QPixmap(os.path.join(path, "dynamic_talking_3.png")),
            "talking_4": QtGui.QPixmap(os.path.join(path, "dynamic_talking_4.png")),
            "talking_eyes": QtGui.QPixmap(os.path.join(path, "dynamic_talking_eyes.png")),
            "talking_bubble_0": QtGui.QPixmap(os.path.join(path, "dynamic_talking_bubble_0.png")),
            "talking_bubble_1": QtGui.QPixmap(os.path.join(path, "dynamic_talking_bubble_1.png")),
            "talking_bubble_2": QtGui.QPixmap(os.path.join(path, "dynamic_talking_bubble_2.png")),
        }

    @staticmethod
    def load_mouse_textures(path):
        path = os.path.join(path, "mouse_cat")

        return {
            "base": QtGui.QPixmap(os.path.join(path, "mouse_cat_base.png")),
            "mouse": QtGui.QPixmap(os.path.join(path, "mouse_cat_mouse.png")),
            "pad": QtGui.QPixmap(os.path.join(path, "mouse_cat_pad.png")),
        }

    @staticmethod
    def load_1k_textures(path, mod, scale):
        path = os.path.join(path, "1k_cat")

        return {
            "0": QtGui.QPixmap(os.path.join(path, "1k_cat" + mod + "_0.png")).scaledToWidth(scale),
            "1": QtGui.QPixmap(os.path.join(path, "1k_cat" + mod + "_1.png")).scaledToWidth(scale),
        }

    @staticmethod
    def load_2k_textures(path):
        path = os.path.join(path, "2k_cat")
        return {
            "base": QtGui.QPixmap(os.path.join(path, "2k_cat_base.png")).scaledToWidth(200),
            "l_0": QtGui.QPixmap(os.path.join(path, "2k_cat_l_0.png")).scaledToWidth(200),
            "l_1": QtGui.QPixmap(os.path.join(path, "2k_cat_l_1.png")).scaledToWidth(200),
            "r_0": QtGui.QPixmap(os.path.join(path, "2k_cat_r_0.png")).scaledToWidth(200),
            "r_1": QtGui.QPixmap(os.path.join(path, "2k_cat_r_1.png")).scaledToWidth(200),
        }

    @staticmethod
    def load_rev_2k_textures(path):
        path = os.path.join(path, "2k_cat")
        return {
            "base": QtGui.QPixmap(os.path.join(path, "2k_cat_base.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
            "r_0": QtGui.QPixmap(os.path.join(path, "2k_cat_l_0.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
            "r_1": QtGui.QPixmap(os.path.join(path, "2k_cat_l_1.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
            "l_0": QtGui.QPixmap(os.path.join(path, "2k_cat_r_0.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
            "l_1": QtGui.QPixmap(os.path.join(path, "2k_cat_r_1.png")).transformed(
                QtGui.QTransform().scale(-1, 1)).scaledToWidth(231),
        }

    @staticmethod
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

    @staticmethod
    def load_rev_4k_textures(path):
        path = os.path.join(path, "4k_cat")
        return {
            "base": QtGui.QPixmap(os.path.join(path, "4k_cat_base.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "r_00": QtGui.QPixmap(os.path.join(path, "4k_cat_l_00.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "r_10": QtGui.QPixmap(os.path.join(path, "4k_cat_l_01.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "r_01": QtGui.QPixmap(os.path.join(path, "4k_cat_l_10.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "r_11": QtGui.QPixmap(os.path.join(path, "4k_cat_l_11.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "l_00": QtGui.QPixmap(os.path.join(path, "4k_cat_r_00.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "l_10": QtGui.QPixmap(os.path.join(path, "4k_cat_r_01.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "l_01": QtGui.QPixmap(os.path.join(path, "4k_cat_r_10.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
            "l_11": QtGui.QPixmap(os.path.join(path, "4k_cat_r_11.png")).transformed(
                QtGui.QTransform().scale(-1, 1)),
        }

    def load_config(self):
        file = open("config.json", "r")
        data = json.load(file)
        self.default_layout = read_layout(data["default_layout"])

        self.enable_dynamic_layout = read_bool(data["enable_dynamic_layout"])

        self.enable_talking = read_bool(data["enable_talking"])

        self.enable_bumpers = read_bool(data["enable_bumpers"])
        self.mouse_type = data["mouse_type"]
        self.enable_dynamic_talking = read_bool(data["enable_dynamic_talking"])

        self.fps = int(data["fps"])
        file.close()

    def load_key_layout(self):
        file = open("input.json", "r")
        data = json.load(file)

        # mouse game with WASD movemement
        mg = data["mouse_game"]
        self.keys["mkg"] = [mg["left_click"], mg["right_click"]]
        mjg = mg["joystick"]
        self.keys["mjg"] = [mjg["stick_left"], mjg["stick_up"], mjg["stick_right"], mjg["stick_down"]]

        # OSU layout
        mo = data["mouse_osu"]
        self.keys["mko"] = [mo["left_button"], mo["right_button"]]

        # mania layout
        mania = data["mania"]
        self.keys["4k"] = mania[0:4]
        self.keys["2k"] = mania[2:4]
        self.keys["1k"] = mania[4]
        self.keys["2k_rev"] = mania[5:7]
        self.keys["4k_rev"] = mania[5:10]
        self.keys["3k"] = mania[3:6]

        # steam controller.
        controller = data["controller"]
        self.keys["bc"] = [controller["down_button"], controller["right_button"], controller["up_button"],
                           controller["left_button"]]
        self.keys["jc"] = [controller["stick_left"], controller["stick_up"], controller["stick_right"],
                           controller["stick_down"]]
        self.keys["lb"] = controller["left_bumper"]
        self.keys["rb"] = controller["right_bumper"]

        # stadia / xbox controller.
        self.keys["stadia_bc"] = ["controller button 2", "controller button 3", "controller button 1",
                                  "controller button 0"]
        self.keys["stadia_jc_1"] = ["controller joystick first horizontal left",
                                    "controller joystick first vertical up",
                                    "controller joystick first horizontal right",
                                    "controller joystick first vertical down"]
        self.keys["stadia_jc_2"] = ["controller joystick second horizontal left",
                                    "controller joystick second vertical up",
                                    "controller joystick second horizontal right",
                                    "controller joystick second vertical down"]
        self.keys["stadia_hat"] = ["controller hat vertical down",
                                   "controller hat horizontal left",
                                   "controller hat vertical up",
                                   "controller hat horizontal right"]
        self.keys["stadia_lb"] = ["controller button 4"]
        self.keys["stadia_rb"] = ["controller button 5"]

        file.close()

        # hardcode the keyboard layout.
        self.keys['kb'] = {
            'kb_00': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            'kb_01': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
#            'kb_01': ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
            'kb_10': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
            'kb_11': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
#            'kb_11': ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}'],
            'kb_20': ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'enter'],
            'kb_21': ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'enter'],
#            'kb_21': ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', 'enter'],
            'kb_30': ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift'],
            'kb_31': ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'right shift'],
#            'kb_31': ['shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', 'right shift'],
        }


booleans = ["true", "false"]
layouts = {
    "mouse": '-',
    "controller": '`',
    "keyboard": '=',
    "talk": '0',
    "1-key": '1',
    "2-key": '2',
    "3-key": '3',
    "4-key": '4',
    "5-key": '5',
    "6-key": '6',
    "7-key": '7',
    "8-key": '8',
    "9-key": '9',
    "generic_controller": 'backspace',
}


def read_bool(word):
    if word not in booleans:
        raise ValueError("incorrect value in config file: '" + word + " not in " + "".join(booleans))
    return word == 'true'


def read_layout(word):
    if word not in layouts.keys():
        raise ValueError("incorrect value in config file: '" + word + " not in " + "".join(layouts.keys()))
    return layouts[word]
