import config
from notifications import NotificationsBridge
from popup import Popup
from network import NetworkManager
from view import View
from PyQt5.QtCore import Qt, QUrl, QUrlQuery
from PyQt5.QtGui import QIcon, QDesktopServices
# from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebInspector
from PyQt5.QtWidgets import (QApplication, QAction, QMenu, QShortcut,
                             QSplitter, QSystemTrayIcon, QVBoxLayout,
                             QWidget)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.createAction()
        self.createTrayIcon()
        self.setIcon()
        self.trayIcon.show()

        self.setupView()
        self.setupNAM()
        self.view.load(QUrl(config.WX_URL))
        self.setupInspector()

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)

        self.popup = Popup(self.showFront, self)

    def setupView(self):
        self.view = View(self)
        self.view.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScript)
        self.view.linkClicked[QUrl].connect(self.openURL)

    def setupNAM(self):
        self.nam = NetworkManager(self)
        self.view.page().setNetworkAccessManager(self.nam)

    def setupInspector(self):
        page = self.view.page()
        self.webInspector = QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QShortcut(self)
        shortcut.setKey(Qt.Key_F12)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())

    def showFront(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.activateWindow()
        self.show()

    def iconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.showFront()

    def createAction(self):
        self.restoreAction = QAction("Restore", self,
                                     triggered=self.showFront)
        self.quitAction = QAction("Quit", self,
                                  triggered=QApplication.instance().quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.activated.connect(self.iconActivated)

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
