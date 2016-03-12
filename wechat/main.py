import sys

from PyQt5.QtWidgets import QApplication, QShortcut, QSplitter, QVBoxLayout, \
        QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebInspector, QWebView


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = QWebView(self)
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


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.view.load(QUrl('https://wx.qq.com'))
    app.exec_()

if __name__ == "__main__":
    main()
