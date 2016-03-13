import sys
import os
from qwechat import icon_path
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebInspector, QWebView
from PyQt5.QtWidgets import (QApplication, QAction, QMenu, QShortcut,
                             QSplitter, QSystemTrayIcon, QVBoxLayout,
                             QWidget)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.createAction()
        self.createTrayIcon()
        self.setIcon()
        self.trayIcon.show()
        self.trayIcon.activated.connect(self.iconActivated)

        zoom_factor = self.physicalDpiX() * 0.008
        self.view = QWebView(self)
        self.view.setZoomFactor(zoom_factor)
        self.view.settings().setAttribute(
            QWebSettings.LocalStorageEnabled, True)

        self.setupInspector()

        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)

        layout = QVBoxLayout(self)
        layout.addWidget(self.splitter)

        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)

    def setupInspector(self):
        page = self.view.page()
        page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QShortcut(self)
        shortcut.setKey(Qt.Key_F12)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())

    def iconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.showNormal()

    def createAction(self):
        self.restoreAction = QAction("&Restore", self,
                                     triggered=self.showNormal)
        self.quitAction = QAction("&Quit", self,
                                  triggered=QApplication.instance().quit)

    def setIcon(self):
        icon = QIcon(os.path.join(icon_path, 'qwechat.png'))
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setContextMenu(self.trayIconMenu)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('QWeChat')
    window = Window()
    window.showMaximized()
    window.view.load(QUrl('https://wx.qq.com'))
    app.exec_()

if __name__ == "__main__":
    main()
