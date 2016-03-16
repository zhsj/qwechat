from PyQt5.QtCore import QStandardPaths, QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkDiskCache


class NetworkManager(QNetworkAccessManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        cache_dir = QStandardPaths.writableLocation(
            QStandardPaths.CacheLocation)
        disk_cache = QNetworkDiskCache(self)
        disk_cache.setCacheDirectory(cache_dir)
        self.setCache(disk_cache)

    def getCache(self, url):
        return self.cache().data(QUrl(url))
