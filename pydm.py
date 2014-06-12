from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QUrl, QFileInfo, QFile, QDir, QIODevice
from PyQt4.QtGui import QApplication, QDialog, QProgressBar, QLabel, QPushButton, QDialogButtonBox, \
                    QVBoxLayout, QMessageBox
from PyQt4.QtNetwork import QHttp

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Downloader(QtGui.QMainWindow):
    
    def setupUi(self, downloader):
        downloader.setObjectName(_fromUtf8("downloader"))
        downloader.resize(619, 270)
        self.centralwidget = QtGui.QWidget(downloader)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 31, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.url_text = QtGui.QLineEdit(self.centralwidget)
        self.url_text.setGeometry(QtCore.QRect(90, 20, 411, 27))
        self.url_text.setObjectName(_fromUtf8("url_text"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txt_location = QtGui.QLineEdit(self.centralwidget)
        self.txt_location.setGeometry(QtCore.QRect(90, 60, 211, 27))
        self.txt_location.setObjectName(_fromUtf8("txt_location"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 130, 581, 80))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.progressBar = QtGui.QProgressBar(self.frame_2)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 561, 61))
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 581, 91))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.button_start = QtGui.QPushButton(self.frame)
        self.button_start.setGeometry(QtCore.QRect(500, 10, 71, 31))
        self.button_start.setObjectName(_fromUtf8("button_start"))
        self.closebutton = QtGui.QPushButton(self.frame)
        self.closebutton.setGeometry(QtCore.QRect(500, 50, 71, 31))
        self.closebutton.setObjectName(_fromUtf8("closebutton"))
        self.button_browse = QtGui.QPushButton(self.frame)
        self.button_browse.setGeometry(QtCore.QRect(300, 50, 81, 27))
        self.button_browse.setObjectName(_fromUtf8("button_browse"))
        downloader.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(downloader)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 619, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        downloader.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(downloader)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        downloader.setStatusBar(self.statusbar)

        self.retranslateUi(downloader)
        QtCore.QMetaObject.connectSlotsByName(downloader)

    def retranslateUi(self, downloader):
        downloader.setWindowTitle(QtGui.QApplication.translate("downloader", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("downloader", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("downloader", "Save to", None, QtGui.QApplication.UnicodeUTF8))
        self.button_start.setText(QtGui.QApplication.translate("downloader", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.closebutton.setText(QtGui.QApplication.translate("downloader", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.button_browse.setText(QtGui.QApplication.translate("downloader", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.statusbar.showMessage("Preparing")

        
    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent)
        self.setupUi(self)
 
        self.httpGetId = 0
        self.httpRequestAborted = False
                        
        self.http = QHttp(self)
        self.http.requestFinished.connect(self.httpRequestFinished)
        self.http.dataReadProgress.connect(self.updateDataReadProgress)
        self.http.responseHeaderReceived.connect(self.readResponseHeader)
        self.closebutton.clicked.connect(self.cancelDownload)
        self.button_browse.clicked.connect(self.open_file)
        self.button_start.clicked.connect(self.downloadFile)

    
        self.setWindowTitle('Download Example')

    def open_file(self):
        fd = QtGui.QFileDialog(self)
        self.loc = str(fd.getExistingDirectory())
        self.txt_location.setText(self.loc)
      
        
    def downloadFile(self):
        
        url = QUrl(self.url_text.text())
        if self.txt_location.text()=="":
            QDir.setCurrent("$HOME/Downloads")
        else:
            QDir.setCurrent(self.loc)

        self.statusbar.showMessage("Downloading")
        
        fileInfo = QFileInfo(url.path())
        fileName = fileInfo.fileName()

        if QFile.exists(fileName):
            QFile.remove(fileName)

        self.outFile = QFile(fileName)
        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, 'Error',
                    'Unable to save the file %s: %s.' % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        mode = QHttp.ConnectionModeHttp
        port = url.port()
        if port == -1:
            port = 0
        self.http.setHost(url.host(), mode, port)
        self.httpRequestAborted = False

        path = QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            path = str(path)
        else:
            path = '$HOME/Downloads'

        # Download the file.
        self.httpGetId = self.http.get(path, self.outFile)

    def cancelDownload(self):
        self.statusbar.showMessage("Download canceled")
        self.httpRequestAborted = True
        self.http.abort()

    def httpRequestFinished(self, requestId, error):
        if requestId != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None
            return

        self.outFile.close()

        if error:
            self.outFile.remove()
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % self.http.errorString())

        self.statusbar.showMessage("Download Finished")

    def readResponseHeader(self, responseHeader):
        # Check for genuine error conditions.
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            QMessageBox.information(self, 'Error',
                    'Download failed: %s.' % responseHeader.reasonPhrase())
            self.httpRequestAborted = True
            self.http.abort()

    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted:
            return
        self.progressBar.setMaximum(totalBytes)
        self.progressBar.setValue(bytesRead)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())