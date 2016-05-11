import config
from PyQt5.QtNetwork import QNetworkProxy


proxy = QNetworkProxy()
if not config.PROXY_ENABLE:
    proxy.setType(QNetworkProxy.NoProxy)
else:
    proxy_type = config.PROXY_INFO[0]
    if proxy_type == "socks5":
        proxy.setType(QNetworkProxy.Socks5Proxy)
        proxy.setHostName(config.PROXY_INFO[1])
        proxy.setPort(config.PROXY_INFO[2])
    else:
        raise Exception("Not implemented proxy type")
