import sys
import config
from window import Window
from PyQt5.QtWidgets import QApplication


def runApp():
    if config.DEBUG:
        sys.argv.append("--remote-debugging-port=" + str(config.DEBUG_PORT))
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    window.showMaximized()
    app.exec_()

if __name__ == "__main__":
    sys.exit(runApp())
