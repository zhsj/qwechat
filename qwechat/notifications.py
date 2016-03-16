import config
from PyQt5.QtCore import QObject, pyqtSlot


class NotificationsBridge(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        # self.trayIcon = parent.trayIcon
        self.parent = parent
        self.popup = parent.popup

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    @pyqtSlot(str, str, str)
    def showMsg(self, title, msg="", icon=""):
        # self.trayIcon.showMessage(title, msg)
        icon_url = config.WX_URL.rstrip('/') + '/' + icon.lstrip('/')
        icon_img = self.parent.nam.getCache(icon_url)
        self.popup.updateInfo(title, msg, icon_img)
        self.popup.show()
