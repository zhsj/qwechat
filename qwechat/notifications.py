import config
from PyQt5.QtCore import QObject, pyqtSlot


class NotificationsBridge(QObject):
    def __init__(self, nam, popup, parent=None):
        super().__init__(parent)
        self.nam = nam
        self.popup = popup

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    @pyqtSlot(str, str, str)
    def showMsg(self, title, msg="", icon=""):
        icon_url = config.WX_URL.rstrip('/') + '/' + icon.lstrip('/')
        icon_img = self.nam.getCache(icon_url)
        self.popup.updateInfo(title, msg, icon_img)
        self.popup.show()
