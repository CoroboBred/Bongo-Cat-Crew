import keyboard
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.cat_configs = config.cat_configs

        self.stack = QtWidgets.QStackedWidget()
        self.layout_indices = {}
        self.cat_layouts = {}
        index = 0
        for layout_key in self.cat_configs:
            layout = QtWidgets.QHBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
            container = QtWidgets.QWidget()
            container.setLayout(layout)
            self.stack.addWidget(container)
            self.layout_indices[layout_key] = index
            self.cat_layouts[layout_key] = layout
            index = index + 1

        self.curr_layout = '-'
        self.set_cat_layout(self.curr_layout)  # Default to using the mouse cat layout.
        self.setCentralWidget(self.stack)
        self.setStyleSheet("background-color: green;")
        self.setWindowTitle("Bongo cat")
        self.set_width()

        config.timer.timeout.connect(self.update)
        self.show()

    def set_width(self):
        max_width = 0
        for key in self.cat_configs:
            width = 0
            for cat in self.cat_configs[key]:
                width = width + cat.width()
            max_width = max(width, max_width)
        self.setFixedWidth(max_width)

    def update(self):
        # when using the joystick layout, only allow switching to the mouse layout due to conflicting input keys.
        if self.curr_layout == '`':
            if keyboard.is_pressed('-'):
                self.set_cat_layout('-')
            return
        for key in self.cat_configs:
            if keyboard.is_pressed(key):
                self.set_cat_layout(key)

    def set_cat_layout(self, key):
        self.curr_layout = key
        self.stack.setCurrentIndex(self.layout_indices[key])

        layout = self.cat_layouts[key]
        buffer = QtWidgets.QWidget()
        buffer.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        layout.addWidget(buffer)
        for cat in self.cat_configs[key]:
            layout.addWidget(cat, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

