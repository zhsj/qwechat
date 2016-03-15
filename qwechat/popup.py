import sys
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QGridLayout)


class Popup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.X11BypassWindowManagerHint |
                            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)
        self.setupGeo()
        self.addLayout()
        self.setStyleSheet('''
                QWidget { background: white; }
                ''')

    def setupGeo(self):
        availRect = QApplication.desktop().availableGeometry()
        rect = QRect(0, 0, 300, 100)
        rect.moveBottomRight(availRect.bottomRight() - QPoint(5, 5))
        self.setGeometry(rect)

    def addLayout(self):
        self.avatar = QLabel(self)
        self.title = QLabel(self)
        self.text = QLabel(self)
        closeBtn = QPushButton(self)
        closeBtn.clicked.connect(self.close)
        layout = QGridLayout(self)
        layout.addWidget(self.avatar, 0, 0, 2, 1, Qt.AlignLeft)
        layout.addWidget(self.title, 0, 1, 1, 1, Qt.AlignLeft)
        layout.addWidget(closeBtn, 0, 2, 1, 1, Qt.AlignRight)
        layout.addWidget(self.text, 1, 1, 2, 2, Qt.AlignLeft)
        self.setLayout(layout)

    def updateInfo(self, title, text="", icon=None):
        self.title.setText(title)
        self.text.setText(text)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    window = Popup()
    window.show()
    sys.exit(app.exec_())
