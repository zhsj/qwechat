from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebPage


class View(QWebView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setZoomFactor(self.physicalDpiX() * 0.008)
        page = self.page()
        page.setFeaturePermission(page.mainFrame(), QWebPage.Notifications,
                                  QWebPage.PermissionGrantedByUser)
        page.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)

        # BUG(zhsj): Still can't use copy func in wechat menu
        page.settings().setAttribute(QWebSettings.JavascriptCanAccessClipboard,
                                     True)
        page.featurePermissionRequested.connect(self.permissionRequested)
        page.setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

    def permissionRequested(self, frame, feature):
        self.page().setFeaturePermission(
            frame, feature, QWebPage.PermissionGrantedByUser)
