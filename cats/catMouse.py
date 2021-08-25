from PyQt5 import QtWidgets, QtGui, QtCore  # import PyQt5 widgets

from cats import cat
import pyautogui


class CatMouse(cat.Cat):
    def __init__(self, textures, timer):
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

        timer.timeout.connect(self.update_mouse)

    def update_mouse(self):
        pix_map = self.textures["base"].copy()
        painter = QtGui.QPainter(pix_map)
        mouse_pad = self.textures["pad"].copy()
        mouse_pad = mouse_pad.scaledToHeight(int(self.h / 2))
        x_offset = 10
        y_offset = 0
        painter.drawPixmap(self.w - mouse_pad.width() - x_offset, self.h - mouse_pad.height() - y_offset, mouse_pad)

        x_cursor, y_cursor = pyautogui.position()
        x_cursor, y_cursor = max(0, x_cursor), max(0, y_cursor)
        mouse_map = self.textures["mouse"].copy()
        mouse_map = mouse_map.scaledToHeight(int(mouse_pad.height() / 3.5))
        x_mouse = int(
            (x_cursor / self.res_x * (mouse_pad.width() - mouse_map.width())) - x_offset + self.w - mouse_pad.width())
        y_mouse = int((y_cursor / self.res_y * (
                mouse_pad.height() - mouse_map.height() - mouse_map.height())) - y_offset + self.h - mouse_pad.height() + (mouse_map.height()/2))

        painter.drawPixmap(x_mouse, y_mouse, mouse_map)

        x, y = 120, 210  # x, y coordinates of where to start the arm.

        fx = x_mouse / ((mouse_pad.width() - mouse_map.width()) - x_offset + self.w - mouse_pad.width())
        fy = y_mouse / ((mouse_pad.height() - mouse_map.height() - mouse_map.height()) - y_offset + self.h - mouse_pad.height() + mouse_map.height())
        self.draw_arm(painter, x_mouse + (120 * fx), y_mouse + (70 * fy), x, y, x + 70, y - 30, -50)

        x, y = 240, 180
        self.draw_arm(painter, x_mouse + (60 * fx), y_mouse + (90 * fy), x, y, x + 70, y - 10, -100)
        painter.end()

        self.label.setPixmap(pix_map)
        self.layout.addWidget(self.label)

    def width(self):
        return self.w

    def arm_poly(self, x_arm, y_arm, x_mouse, y_mouse, arm_width):
        return QtGui.QPolygonF([QtCore.QPointF(x_arm, y_arm), QtCore.QPointF(x_mouse, y_mouse),
                                QtCore.QPointF(x_mouse + arm_width, y_mouse - arm_width),
                                QtCore.QPointF(x_arm + arm_width, y_arm - arm_width)])

    def draw_arm(self, painter, x_mouse, y_mouse, x_paw_start, y_paw_start, x_paw_end, y_paw_end, wobble_factor):
        path = QtGui.QPainterPath()
        x_mid = (x_paw_start + x_paw_end)/2
        y_mid = (y_paw_start + y_paw_end)/2
        wobble_y = (x_mouse - x_mid)/wobble_factor
        wobble_x = (y_mouse - y_mid)/wobble_factor
        path.moveTo(x_paw_start - wobble_x, y_paw_start - wobble_y)
        path.cubicTo(x_mouse - 20, y_mouse + 20, x_mouse + 20, y_mouse - 20, x_paw_end + wobble_x, y_paw_end + wobble_y)

        brush = QtGui.QBrush()
        brush.setColor(QtCore.Qt.white)
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(5)
        painter.setPen(pen)
        path.setFillRule(QtCore.Qt.WindingFill)
        painter.drawPath(path)
