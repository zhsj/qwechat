import os

WX_URL = "https://wx.qq.com"
APP_NAME = "QWeChat"
icon_path = 'icons/'
try:
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'icons')
except:
    pass
