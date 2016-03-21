import config
from notifications import NotificationsBridge
from popup import Popup
from network import NetworkManager
from view import View
from tray import TrayIcon
from inspector import Inspector
from PyQt5.QtCore import Qt, QUrl, QUrlQuery
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWidgets import QApplication, QSplitter, QVBoxLayout, QWidget


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupTrayIcon()
        self.setIcon()
        self.trayIcon.show()

        self.setupView()
        self.setupNAM()
        self.nam.loadCookie()
        self.view.load(QUrl(config.WX_URL))
        self.setupLayout()

        self.popup = Popup(self.showFront, self)

    def setupView(self):
        self.view = View(self)
        self.view.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScript)
        self.view.linkClicked[QUrl].connect(self.openURL)

    def setupNAM(self):
        self.nam = NetworkManager(self)
        self.view.page().setNetworkAccessManager(self.nam)

    def setupLayout(self):
        layout = QVBoxLayout(self)
        if config.DEBUG:
            self.view.page().settings().setAttribute(
                QWebSettings.DeveloperExtrasEnabled, True)
            webInspector = Inspector(self)
            webInspector.setPage(self.view.page())
            self.splitter = QSplitter(self)
            self.splitter.setOrientation(Qt.Vertical)
            self.splitter.addWidget(self.view)
            self.splitter.addWidget(webInspector)
            layout.addWidget(self.splitter)
        else:
            layout.addWidget(self.view)

    def showFront(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.activateWindow()
        self.show()

    def quitApp(self):
        self.nam.saveCookie()
        QApplication.instance().quit()

    def setupTrayIcon(self):
        self.trayIcon = TrayIcon(self)
        self.trayIcon.setup(self, self.showFront, self.quitApp)

    def setIcon(self):
        icon = QIcon(config.icon_path)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

    def populateJavaScript(self):
        notificatonsBridge = NotificationsBridge(self.nam, self.popup, self)
        frame = self.view.page().mainFrame()
        frame.addToJavaScriptWindowObject("notify", notificatonsBridge)
        with open(config.inject_js_path, "r") as f:
            injectJS = f.read()
        frame.evaluateJavaScript(injectJS)

    def openURL(self, url):
        if QUrl(config.WX_URL).isParentOf(url):
            query = QUrlQuery(url)
            if query.hasQueryItem("requrl"):
                requrl = query.queryItemValue("requrl", QUrl.FullyDecoded)
                QDesktopServices.openUrl(QUrl(requrl))
