import sys
import config
from window import Window
from PyQt5.QtWidgets import QApplication


def runApp():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    window = Window()
    window.showMaximized()
    app.exec_()

if __name__ == "__main__":
    sys.exit(runApp())
