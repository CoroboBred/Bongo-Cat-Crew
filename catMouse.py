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
        x_offset = 250
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

        x, y = 450, 220
        self.draw_arm(painter, x_mouse + 60, y_mouse + 60, x, y, x + 50, y - 30)


#        x, y = 650, 150
#        self.draw_arm(painter, x_mouse + 60, y_mouse + 60, x, y, x - 50, y + 30)
        painter.end()

        self.label.setPixmap(pix_map)
        self.layout.addWidget(self.label)

    def width(self):
        self.w

    def arm_poly(self, x_arm, y_arm, x_mouse, y_mouse, arm_width):
        return QtGui.QPolygonF([QtCore.QPointF(x_arm, y_arm), QtCore.QPointF(x_mouse, y_mouse),
                                QtCore.QPointF(x_mouse + arm_width, y_mouse - arm_width),
                                QtCore.QPointF(x_arm + arm_width, y_arm - arm_width)])

    def draw_arm(self, painter, x, y, x_paw_start, y_paw_start, x_paw_end, y_paw_end):
        # initializing pss and pss2 (kuvster's magic)
        path = QtGui.QPainterPath()
        oof = 6

        pss = [float(x_paw_start), float(y_paw_start)]
        dist = math.hypot(x_paw_start - x, y_paw_start - y)
        centreleft0 = x_paw_start - 0.7237 * dist / 2
        centreleft1 = y_paw_start + 0.69 * dist / 2
        for i in range(1, oof):
            bez = [float(x_paw_start), float(y_paw_start), centreleft0, centreleft1, x, y]
            p0, p1 = self.bezier(1.0 * i / oof, bez, 6)
            pss.append(p0)
            pss.append(p1)

        pss.append(x)
        pss.append(y)
        a = y - centreleft1
        b = centreleft0 - x
        le = math.hypot(a, b)
        a = x + a / le * 60
        b = y + b / le * 60
        dist = math.hypot(x_paw_end - a, y_paw_end - b)
        centreright0 = x_paw_end - 0.6 * dist / 2
        centreright1 = y_paw_end + 0.8 * dist / 2
        push = 20
        s = x - centreleft0
        t = y - centreleft1
        le = math.hypot(s, t)
        s *= push / le
        t *= push / le
        s2 = a - centreright0
        t2 = b - centreright1
        le = math.hypot(s2, t2)
        s2 *= push / le
        t2 *= push / le
        for i in range(1, oof):
            bez = [x, y, x + s, y + t, a + s2, b + t2, a, b]
            p0, p1 = self.bezier(1.0 * i / oof, bez, 8)
            pss.append(p0)
            pss.append(p1)

        pss.append(a)
        pss.append(b)
        for i in range(oof - 1, 0, -1):
            bez = [1.0 * x_paw_end, 1.0 * y_paw_end, centreright0, centreright1, a, b]
            p0, p1 = self.bezier(1.0 * i / oof, bez, 6)
            pss.append(p0)
            pss.append(p1)

        pss.append(x_paw_end)
        pss.append(y_paw_end)
        mpos0 = (a + x) / 2 - 52 - 15
        mpos1 = (b + y) / 2 - 34 + 5
        dx = 0
        dy = 0

        iter = 25

        pss2 = [pss[0] + dx, pss[1] + dy]
        for i in range(1, iter):
            p0, p1 = self.bezier(1.0 * i / iter, pss, 38)
            pss2.append(p0 + dx)
            pss2.append(p1 + dy)

        pss2.append(pss[36] + dx)
        pss2.append(pss[37] + dy)

        # offset set to zero because I don't think we need it. maybe change later
        offset_x = 0
        offset_y = 0
        fill = [QtCore.QPointF(mpos0 + dx + offset_x, mpos1 + dy + offset_y)]

        # drawing arms
        for i in range(0, 26, 2):
            fill.append(QtCore.QPointF(pss2[i], pss2[i + 1]))
            fill.append(QtCore.QPointF(pss2[52 - i - 2], pss2[52 - i - 1]))
        path.addPolygon(QtGui.QPolygonF(fill))

        # drawing first arm arc
        width = 6
        path.addEllipse(pss2[0] - width / 2, pss2[1] - width / 2, width / 2, width / 2)
        edge = QtGui.QPolygonF()
        for i in range(0, 50, 2):
            vec0 = pss2[i] - pss2[i + 2]
            vec1 = pss2[i + 1] - pss2[i + 3]
            dist = math.hypot(vec0, vec1)
            edge.append(QtCore.QPointF(pss2[i] + vec1 / dist * width / 2, pss2[i + 1] - vec0 / dist * width / 2))
            edge.append(QtCore.QPointF(pss2[i] - vec1 / dist * width / 2, pss2[i + 1] + vec0 / dist * width / 2))
            width -= 0.08

        vec0 = pss2[50] - pss2[48]
        vec1 = pss2[51] - pss2[49]
        dist = math.hypot(vec0, vec1)
        edge.append(QtCore.QPointF(pss2[50] + vec1 / dist * width / 2, pss2[51] - vec0 / dist * width / 2))
        edge.append(QtCore.QPointF(pss2[50] - vec1 / dist * width / 2, pss2[51] + vec0 / dist * width / 2))
        path.addPolygon(QtGui.QPolygonF(edge))
        path.addEllipse(pss2[50] - width / 2, pss2[51] - width / 2, width / 2, width / 2)

        # drawing second arm arc
        edge2 = []
        width = 6
        path.addEllipse(pss2[0] - width / 2, pss2[1] - width / 2, width / 2, width / 2)
        for i in range(0, 50, 2):
            vec0 = pss2[i] - pss2[i + 2]
            vec1 = pss2[i + 1] - pss2[i + 3]
            dist = math.hypot(vec0, vec1)
            edge2.append(QtCore.QPointF(pss2[i] + vec1 / dist * width / 2, pss2[i + 1] - vec0 / dist * width / 2))
            edge2.append(QtCore.QPointF(pss2[i] - vec1 / dist * width / 2, pss2[i + 1] + vec0 / dist * width / 2))
            width -= 0.08

        vec0 = pss2[50] - pss2[48]
        vec1 = pss2[51] - pss2[49]
        dist = math.hypot(vec0, vec1)
        edge2.append(QtCore.QPointF(pss2[50] + vec1 / dist * width / 2, pss2[51] - vec0 / dist * width / 2))
        edge2.append(QtCore.QPointF(pss2[50] - vec1 / dist * width / 2, pss2[51] + vec0 / dist * width / 2))
        path.addPolygon(QtGui.QPolygonF(edge2))

        path.addEllipse(pss2[50] - width / 2, pss2[51] - width / 2, width / 2, width / 2)

        brush = QtGui.QBrush()
        brush.setColor(QtCore.Qt.white)
        brush.setStyle(QtCore.Qt.SolidPattern)
        painter.setBrush(brush)
        pen = QtGui.QPen()
        pen.setColor(QtCore.Qt.red)
        pen.setWidth(5)
        painter.setPen(pen)
        path.setFillRule(QtCore.Qt.WindingFill)
        painter.drawPath(path)

    # bezier curve for osu
    def bezier(self, ratio, points, length):
        fact = [0.001, 0.001, 0.002, 0.006, 0.024, 0.12, 0.72, 5.04, 40.32, 362.88, 3628.8, 39916.8, 479001.6,
                6227020.8, 87178291.2, 1307674368.0, 20922789888.0, 355687428096.0, 6402373705728.0,
                121645100408832.0, 2432902008176640.0, 51090942171709440.0]
        nn = int(length / 2) - 1
        xx = 0
        yy = 0

        for point in range(nn+1):
            tmp = fact[nn] / (fact[point] * fact[nn - point]) * pow(ratio, point) * pow(1 - ratio, nn - point)
            xx += points[2 * point] * tmp
            yy += points[2 * point + 1] * tmp

        return xx / 1000, yy / 1000
