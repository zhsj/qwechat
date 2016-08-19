from PyQt5.QtCore import QUrl, QUrlQuery
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest
from downloader import Downloader
from network import NetworkManager


class View(QWebView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nam = NetworkManager(self)
        downloader = Downloader(self, self.nam)
        page = Page(self)
        page.setNetworkAccessManager(self.nam)
        page.setFeaturePermission(page.mainFrame(), QWebPage.Notifications,
                                  QWebPage.PermissionGrantedByUser)
        page.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)

        # BUG(zhsj): Still can't use copy func in wechat menu
        page.settings().setAttribute(QWebSettings.JavascriptCanAccessClipboard,
                                     True)
        page.featurePermissionRequested.connect(self.permissionRequested)
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        page.setForwardUnsupportedContent(True)
        page.linkClicked[QUrl].connect(self.openURL)
        page.unsupportedContent[QNetworkReply].connect(downloader.saveFile)
        page.downloadRequested[QNetworkRequest].connect(
            downloader.startDownload)
        self.setPage(page)
        self.setZoomFactor(self.physicalDpiX() * 0.008)

    def openURL(self, url):
        query = QUrlQuery(url)
        if query.hasQueryItem("requrl"):
            orig_url = query.queryItemValue("requrl", QUrl.FullyDecoded)
            url = QUrl(orig_url)
        QDesktopServices.openUrl(url)

    def permissionRequested(self, frame, feature):
        self.page().setFeaturePermission(
            frame, feature, QWebPage.PermissionGrantedByUser)


class Page(QWebPage):
    def __init__(self, parent=None):
        super().__init__()

    def userAgentForUrl(self, url):
        return ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/54.0.2810.2 Safari/537.36")

    def acceptNavigationRequest(self, frame, req, _type):
        if req.url().url().endswith('fake'):
            return False
        return super().acceptNavigationRequest(frame, req, _type)
