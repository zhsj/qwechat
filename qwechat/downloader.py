from PyQt5.QtCore import QCoreApplication, QFile, QIODevice, QObject
from PyQt5.QtWidgets import QFileDialog


class Downloader(QObject):

    def __init__(self, parent, nam):
        super().__init__(parent)

        self.nam = nam
        self.reply = None
        self.downloads = {}
        self.path = ""
        self.parent = parent

    def startDownload(self, req):
        reply = self.nam.get(req)
        reply.finished.connect(self.finishDownload)

    def saveFile(self, reply):
        disposition = reply.rawHeader(b"Content-Disposition").data().decode()
        disposition = disposition.replace(' ', '')
        filenames = [i.split('=')[-1] for i in disposition.split(';')
                     if i.startswith('filename=')]
        filename = ""
        if len(filenames) > 0:
            filename = filenames[0]
        filename = filename.replace('"', '')
        print(filename)
        path, _ = QFileDialog.getSaveFileName(
            self.parent, QCoreApplication.translate("Downloader", "Save File"),
            filename)

        if len(path) != 0:
            file = QFile(path)
            if file.open(QIODevice.WriteOnly):
                file.write(reply.readAll())
                file.close()

    def finishDownload(self):
        reply = self.sender()
        self.saveFile(reply)
        reply.deleteLater()
