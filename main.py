import sys

import window
from PyQt5 import QtWidgets

import read


def main():
    app = QtWidgets.QApplication(sys.argv)

    config = read.Config()

    win = window.MainWindow(config)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
