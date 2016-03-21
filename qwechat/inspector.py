from PyQt5.QtCore import Qt
from PyQt5.QtWebKitWidgets import QWebInspector
from PyQt5.QtWidgets import QShortcut


class Inspector(QWebInspector):
    def __init__(self, parent=None):
        super().__init__(parent)
        shortcut = QShortcut(parent or self)
        shortcut.setKey(Qt.Key_F12)
        self.setVisible(False)

        def toggleInspector():
            self.setVisible(not self.isVisible())
        shortcut.activated.connect(toggleInspector)
