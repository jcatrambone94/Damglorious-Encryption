
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(670, 150)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.Decrypt_Button = QtGui.QPushButton(self.centralwidget)
        self.Decrypt_Button.setMinimumSize(QtCore.QSize(125, 125))
        self.Decrypt_Button.setObjectName(_fromUtf8("Decrypt_Button"))
        self.horizontalLayout.addWidget(self.Decrypt_Button)
        self.Encrypt_Button = QtGui.QPushButton(self.centralwidget)
        self.Encrypt_Button.setMinimumSize(QtCore.QSize(0, 125))
        self.Encrypt_Button.setObjectName(_fromUtf8("Encrypt_Button"))
        self.horizontalLayout.addWidget(self.Encrypt_Button)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Damglorious Encryption Tool", None))
        self.Decrypt_Button.setText(_translate("MainWindow", "Decrypt", None))
        self.Encrypt_Button.setText(_translate("MainWindow", "Encrypt", None))

