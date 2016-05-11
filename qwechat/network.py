import os
import json
from PyQt5.QtCore import QStandardPaths, QUrl
from PyQt5.QtNetwork import (QNetworkAccessManager, QNetworkDiskCache,
                             QNetworkCookie, QNetworkCookieJar)
from proxy import proxy


class NetworkManager(QNetworkAccessManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cookie_jar = QNetworkCookieJar()
        self.cache_dir = QStandardPaths.writableLocation(
            QStandardPaths.CacheLocation)
        self.cookie_file = os.path.join(self.cache_dir, 'cookie.json')
        disk_cache = QNetworkDiskCache(self)
        disk_cache.setCacheDirectory(self.cache_dir)
        self.setCache(disk_cache)
        self.setCookieJar(self.cookie_jar)
        self.setProxy(proxy)

    def getCache(self, url):
        return self.cache().data(QUrl(url))

    def saveCookie(self):
        cookie = [str(c.toRawForm(), 'utf-8')
                  for c in self.cookie_jar.allCookies()]
        jcookie = json.dumps(cookie)
        with open(self.cookie_file, 'w') as f:
            f.write(jcookie)

    def loadCookie(self):
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file, 'r') as f:
                cookie = json.loads(f.read())
            self.cookie_jar.setAllCookies([
                QNetworkCookie.parseCookies(c.encode('utf-8'))[0]
                for c in cookie])
