# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lazydragging_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1064, 277)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("letto256.ico"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 1041, 151))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AlphaFolder = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.AlphaFolder.setObjectName("AlphaFolder")
        self.AlphaFolder.setStyleSheet("background-color: #0057e7")
        self.horizontalLayout.addWidget(self.AlphaFolder)
        self.Settings = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Settings.setObjectName("Settings")
        self.Settings.setStyleSheet("background-color: #ffa700")
        self.horizontalLayout.addWidget(self.Settings)
        self.Merge = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Merge.setObjectName("Merge")
        self.Merge.setStyleSheet("background-color: #008744")
        self.horizontalLayout.addWidget(self.Merge)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 180, 901, 91))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.alpha_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.alpha_label.setObjectName("alpha_label")
        self.horizontalLayout_2.addWidget(self.alpha_label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.setiings_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.setiings_label.setObjectName("setiings_label")
        self.horizontalLayout_2.addWidget(self.setiings_label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("Type folder name")
        self.horizontalLayout_2.addWidget(self.lineEdit, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(930, 210, 111, 31))
        self.SaveButton.setObjectName("SaveButton")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lazy Dragging"))
        self.AlphaFolder.setText(_translate("MainWindow", "Alpha Folder"))
        self.Settings.setText(_translate("MainWindow", "Settings json"))
        self.Merge.setText(_translate("MainWindow", "Merge Button"))
        self.alpha_label.setText(_translate("MainWindow", "Path to alpha folder"))
        self.setiings_label.setText(_translate("MainWindow", "Path to settings.json"))
        self.SaveButton.setText(_translate("MainWindow", "Save pathes"))

