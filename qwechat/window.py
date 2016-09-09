import config
from view import View
from tray import TrayIcon
from proxy import proxy
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtNetwork import QNetworkProxy


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupTrayIcon()
        self.setIcon()
        self.trayIcon.show()

        self.setupView()
        self.view.load(QUrl(config.WX_URL))
        self.view.setZoomFactor(self.physicalDpiX() * 0.008)
        self.setupLayout()

        QNetworkProxy.setApplicationProxy(proxy)

    def setupView(self):
        self.view = View(self)
        self.populateJavaScript()

    def setupLayout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

    def showFront(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.activateWindow()
        self.show()

    def quitApp(self):
        QApplication.instance().quit()

    def setupTrayIcon(self):
        self.trayIcon = TrayIcon(self)
        self.trayIcon.setup(self.showFront, self.quitApp)

    def setIcon(self):
        icon = QIcon(config.icon_path)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

    def populateJavaScript(self):
        with open(config.inject_js_path, "r") as f:
            injectJS = f.read()
        self.view.page().runJavaScript(injectJS)
