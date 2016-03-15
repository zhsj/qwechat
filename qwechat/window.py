import os
import config
from notifications import NotificationsBridge
from popup import Popup
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebInspector, QWebView, QWebPage
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
        self.view.load(QUrl(config.WX_URL))
        self.setupInspector()

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)
        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)

        self.popup = Popup(self)

    def setupView(self):
        self.view = QWebView(self)
        self.view.setZoomFactor(self.physicalDpiX() * 0.008)
        page = self.view.page()
        page.setFeaturePermission(page.mainFrame(), QWebPage.Notifications,
                                  QWebPage.PermissionGrantedByUser)
        page.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        page.featurePermissionRequested.connect(self.permissionRequested)
        page.mainFrame().javaScriptWindowObjectCleared.connect(
            self.populateJavaScript)

    def permissionRequested(self, frame, feature):
        self.view.page().setFeaturePermission(
            frame, feature, QWebPage.PermissionGrantedByUser)

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

        # BUG(zhsj): not triggered
        self.trayIcon.messageClicked.connect(self.messageClicked)

    def messageClicked(self):
        if not self.isVisible():
            self.showFront()

    def setIcon(self):
        icon = QIcon(os.path.join(config.icon_path, 'qwechat.png'))
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

    def populateJavaScript(self):
        notificatonsBridge = NotificationsBridge(self)
        frame = self.view.page().mainFrame()
        frame.addToJavaScriptWindowObject("notify", notificatonsBridge)
        injectJS = """window.Notification = function(title, opts) {
    if(typeof opts === 'undefined') { notify.showMsg(title); }
    else { notify.showMsg(title, opts.body); }
}"""
        frame.evaluateJavaScript(injectJS)
