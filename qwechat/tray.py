from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        trayIconMenu = QMenu(parent)
        self.restoreAction = QAction("Restore", trayIconMenu)
        self.quitAction = QAction("Quit", trayIconMenu)
        trayIconMenu.addAction(self.restoreAction)
        trayIconMenu.addAction(self.quitAction)
        self.setContextMenu(trayIconMenu)

    def setup(self, showCallback, quitCallback):
        def iconActivated(r):
            if r in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
                if callable(showCallback):
                    showCallback()

        self.restoreAction.triggered.connect(showCallback)
        self.quitAction.triggered.connect(quitCallback)
        self.activated.connect(iconActivated)
