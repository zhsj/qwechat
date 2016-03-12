import os

icon_path = 'icons/'
try:
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'icons')
except:
    pass
