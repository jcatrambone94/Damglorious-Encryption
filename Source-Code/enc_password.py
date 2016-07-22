# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Password.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

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

class Ui_passwordWindow(object):
    def setupUi(self, passwordWindow):
        passwordWindow.setObjectName(_fromUtf8("passwordWindow"))
        passwordWindow.resize(620, 278)
        self.centralwidget = QtGui.QWidget(passwordWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 75))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.password = QtGui.QLineEdit(self.centralwidget)
        self.password.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.setObjectName(_fromUtf8("password"))
        self.verticalLayout_3.addWidget(self.password)
        self.confirm = QtGui.QLineEdit(self.centralwidget)
        self.confirm.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm.setFont(font)
        self.confirm.setObjectName(_fromUtf8("confirm"))
        self.verticalLayout_3.addWidget(self.confirm)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        passwordWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(passwordWindow)
        QtCore.QMetaObject.connectSlotsByName(passwordWindow)

    def retranslateUi(self, passwordWindow):
        passwordWindow.setWindowTitle(_translate("passwordWindow", "Damglorious Local Encryption", None))
        self.label.setText(_translate("passwordWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Enter the Password you want to set! </span></p></body></html>", None))
        self.label_3.setText(_translate("passwordWindow", "Password: ", None))
        self.label_4.setText(_translate("passwordWindow", "Confirm:", None))
        self.pushButton.setText(_translate("passwordWindow", "Submit", None))

