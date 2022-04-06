import keyboard
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()
        self.layouts = config.layouts

        self.over_layout = QtWidgets.QGridLayout()
        self.over_layout.setSpacing(0)
        self.over_layout.setContentsMargins(0, 0, 0, 0)
        self.curr_layout_key = config.default_layout
        self.fps = config.fps
        self.timer = config.timer

        self.stack = QtWidgets.QStackedWidget()
        self.layout_indices = {}
        self.q_layouts = {}
        index = 0
        for layout_key in self.layouts:
            layout = QtWidgets.QHBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
            container = QtWidgets.QWidget()
            container.setLayout(layout)
            self.stack.addWidget(container)
            self.layout_indices[layout_key] = index
            self.q_layouts[layout_key] = layout
            index = index + 1

        self.set_cat_layout(self.curr_layout_key)
        self.over_layout.addWidget(self.stack, 0, 0)
        self.overlay_container = QtWidgets.QWidget()
        self.overlay_container.setLayout(self.over_layout)
        self.setCentralWidget(self.overlay_container)
        self.setStyleSheet("background-color: blue;")
        self.setWindowTitle("Bongo Cat")
        self.setWindowIcon(config.icon)
        self.setWindowIconText("Bongo Cat")

        self.set_width()

        if config.enable_dynamic_layout:
            self.timer.timeout.connect(self.update)
        self.show()

    def start(self):
        self.timer.start(1000 // self.fps)

    def set_width(self):
        max_width = 0
        for key in self.layouts:
            width = 0
            for cat in self.layouts[key]:
                width = width + cat.width()
            max_width = max(width, max_width)
        self.setFixedWidth(max_width)

    def update(self):
        if not keyboard.is_pressed("esc"):
            return
        for key in self.layouts:
            if keyboard.is_pressed(key):
                self.set_cat_layout(key)

    def set_cat_layout(self, key):
        self.curr_layout_key = key
        self.stack.setCurrentIndex(self.layout_indices[key])

        layout = self.q_layouts[key]
        buffer = QtWidgets.QWidget()
        buffer.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        layout.addWidget(buffer)
        for cat in self.layouts[key]:
            layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

