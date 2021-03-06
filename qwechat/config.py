import os

WX_URL = "https://wx.qq.com/"
APP_NAME = "QWeChat"
NOTIFY_TIMEOUT = 10000

DEBUG = False
DEBUG_PORT = 8000
if DEBUG:
    WX_URL = WX_URL + '?mmdebug'

PROXY_ENABLE = False
PROXY_INFO = ("socks5", "127.0.0.1", 1080)

icon_path = os.path.join(os.path.dirname(__file__), 'data', 'qwechat.png')
if not os.path.exists(icon_path):
    icon_path = os.path.expanduser("~/.local/share/icons/qwechat.png")

if not os.path.exists(icon_path):
    icon_path = "/usr/local/share/icons/qwechat.png"

inject_js_path = os.path.join(os.path.dirname(__file__), 'data', 'inject.js')


if __name__ == '__main__':
    print(icon_path)
    print(inject_js_path)
