from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, widget, showCallback, quitCallback):
        def iconActivated(r):
            if r in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
                if callable(showCallback):
                    showCallback()

        def createAction():
            self.restoreAction = QAction("Restore", widget,
                                         triggered=showCallback)
            self.quitAction = QAction("Quit", widget,
                                      triggered=quitCallback)

        createAction()
        self.trayIconMenu = QMenu(widget)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.setContextMenu(self.trayIconMenu)
        self.activated.connect(iconActivated)
