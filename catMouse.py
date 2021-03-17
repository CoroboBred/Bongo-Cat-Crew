import math

from PyQt5 import QtWidgets, QtGui, QtCore  # import PyQt5 widgets

import cat
import pyautogui


class CatMouse(cat.Cat):
    def __init__(self, textures):
        super(CatMouse, self).__init__()
        self.textures = textures
        self.label = QtWidgets.QLabel("4k_cat")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.res_x, self.res_y = pyautogui.size()

        self.layout = QtWidgets.QHBoxLayout()
        pix_map = self.textures["base"]
        self.w = pix_map.width()
        self.h = pix_map.height()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.update_mouse()
        self.setLayout(self.layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_mouse)
        self.timer.start(10)

    def update_mouse(self):
        pix_map = self.textures["base"].copy()
        painter = QtGui.QPainter(pix_map)
        mouse_pad = self.textures["pad"].copy()
        mouse_pad = mouse_pad.scaledToHeight(int(self.h / 1.5))
        x_offset = 200
        y_offset = 10
        painter.drawPixmap(self.w - mouse_pad.width() - x_offset, self.h - mouse_pad.height(), mouse_pad)

        x_cursor, y_cursor = pyautogui.position()
        mouse_map = self.textures["mouse"].copy()
        mouse_map = mouse_map.scaledToHeight(int(mouse_pad.height() / 4))
        x_mouse = int(
            (x_cursor / self.res_x * (mouse_pad.width() - mouse_map.width())) - x_offset + self.w - mouse_pad.width())
        y_mouse = int((y_cursor / self.res_y * (
                    mouse_pad.height() - mouse_map.height() - mouse_map.height())) - y_offset + self.h - mouse_pad.height() + mouse_map.height())

        painter.drawPixmap(x_mouse, y_mouse, mouse_map)

        p_path = QtGui.QPainterPath()
        p_path.setFillRule(QtCore.Qt.WindingFill)

        # Draw arm section.
        arm_width = 40
        l_arm = self.arm_poly(420, 200, x_mouse, y_mouse + 60, arm_width)
        r_arm = self.arm_poly(620, 150, x_mouse + 30, y_mouse + 30, arm_width)
        p_path.addPolygon(l_arm)

        brush = QtGui.QBrush()
        brush.setColor(QtCore.Qt.white)
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawPath(p_path)
        painter.end()

        painter = QtGui.QPainter(pix_map)
        brush = QtGui.QBrush()
        brush.setColor(QtCore.Qt.white)
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawPath(p_path)
        p_path = QtGui.QPainterPath()
        p_path.setFillRule(QtCore.Qt.WindingFill)
        p_path.addPolygon(r_arm)
        painter.drawPath(p_path)
        painter.end()

        self.label.setPixmap(pix_map)
        self.layout.addWidget(self.label)

    def width(self):
        self.w

    def arm_poly(self, x_arm, y_arm, x_mouse, y_mouse, arm_width):
        return QtGui.QPolygonF([QtCore.QPointF(x_arm, y_arm), QtCore.QPointF(x_mouse, y_mouse),
                                QtCore.QPointF(x_mouse + arm_width, y_mouse - arm_width),
                                QtCore.QPointF(x_arm + arm_width, y_arm - arm_width)])
