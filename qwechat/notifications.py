from PyQt5.QtCore import QObject, pyqtSlot


class NotificationsBridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.trayIcon = parent.trayIcon

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def showMsg(self, title, msg=""):
        self.trayIcon.showMessage(title, msg)
