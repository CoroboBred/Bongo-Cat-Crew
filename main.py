import sys

from PyQt5 import QtWidgets

import window
import read


def main():
    app = QtWidgets.QApplication(sys.argv)
    config = read.Config()
    win = window.MainWindow(config)
    win.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
