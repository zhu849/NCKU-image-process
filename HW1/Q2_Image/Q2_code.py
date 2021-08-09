# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy
import cv2

def Median_filter():
    img = cv2.imread("cat.png")
    img = cv2.medianBlur(img,7)
    cv2.imshow("Median_filter",img)

def Gaussian_filter():
    img = cv2.imread("cat.png")
    img = cv2.GaussianBlur(img,(3,3),0)
    cv2.imshow("Gaussian_filter",img)
    
def Bilateral_filter():
    img = cv2.imread("cat.png")
    img = cv2.bilateralFilter(img,9,90,90)
    cv2.imshow("Bilateral_filter",img)
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(414, 456)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(60, 40, 281, 321))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 191, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Median_filter)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 130, 191, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Gaussian_filter)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 220, 191, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(Bilateral_filter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 414, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HW - Q2"))
        self.groupBox.setTitle(_translate("MainWindow", "2. Image Smoothing"))
        self.pushButton.setText(_translate("MainWindow", "2.1 Median Filter"))
        self.pushButton_2.setText(_translate("MainWindow", "2.2 Gaussian Blur"))
        self.pushButton_3.setText(_translate("MainWindow", "2.3 Bilateral Filter"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()

