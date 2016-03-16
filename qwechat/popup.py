import sys
import config
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer, QSize
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QGridLayout, QStyle)


class Popup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("container")
        self.parent = parent
        self.setWindowFlags(Qt.Popup | Qt.X11BypassWindowManagerHint |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
                            Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)
        self.setupGeo()
        self.addLayout()
        self.setStyleSheet('''
                QWidget#container { background: white;
                        border: 1px solid #f1f1f1 }
                QLabel#title { font-weight: bold; font-size: 16px }
                QLabel#text { font-size: 16px }
                ''')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close)
        self.timer.start(config.NOTIFY_TIMEOUT)

    def enterEvent(self, event):
        self.timer.stop()

    def leaveEvent(self, event):
        self.timer.start(config.NOTIFY_TIMEOUT)

    def mouseReleaseEvent(self, event):
        if self.parent:
            try:
                self.parent.showFront()
            except:
                pass
        self.close()

    def setupGeo(self):
        self.setFixedSize(300, 100)
        availRect = QApplication.desktop().availableGeometry()
        rect = QRect(0, 0, 300, 100)
        rect.moveBottomRight(availRect.bottomRight() - QPoint(5, 8))
        self.setGeometry(rect)

    def addLayout(self):
        self.icon = QLabel(self)
        self.icon.setObjectName("icon")
        self.title = QLabel(self)
        self.title.setObjectName("title")
        self.text = QLabel(self)
        self.text.setObjectName("text")
        self.text.setWordWrap(True)
        icon = QApplication.style().standardIcon(QStyle.SP_TitleBarCloseButton)
        closeBtn = QPushButton(self)
        closeBtn.setIcon(icon)
        closeBtn.clicked.connect(self.close)
        layout = QGridLayout(self)
        layout.addWidget(self.icon, 0, 0, 2, 1, Qt.AlignCenter)
        layout.addWidget(self.title, 0, 1, 1, 1, Qt.AlignLeft)
        layout.addWidget(closeBtn, 0, 2, 1, 1, Qt.AlignRight)
        layout.addWidget(self.text, 1, 1, 2, 2, Qt.AlignLeft)
        self.setLayout(layout)

    def updateInfo(self, title, text="", icon=None):
        if icon:
            image_reader = QImageReader(icon)
            image_reader.setScaledSize(QSize(80, 80))
            self.icon.setPixmap(QPixmap.fromImageReader(image_reader))
        self.title.setText(title)
        self.text.setText(text)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = Popup()
    window.show()
    sys.exit(app.exec_())
