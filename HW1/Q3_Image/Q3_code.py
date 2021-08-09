# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import math

def Gasussian_Blau():
    img = cv2.imread('Chihiro.jpg',0)
    G = [[(-1,-1),(0,-1),(1,-1)],[(-1,0),(0,0),(1,0)],[(-1,1),(0,1),(1,1)]]
    GN = np.empty((3,3))
    Gnorm = [(0.045,0.122,0.045),(0.122,0.332,0.122),(0.045,0.122,0.045)]
    sigma = 0.9
    for i in range(0,3):
        for j in range(0,3):
            GN[i][j] = math.exp(-1* (G[i][j][0]*G[i][j][0] + G[i][j][1]*G[i][j][1])/2*sigma*sigma) / 2*math.pi*sigma*sigma*Gnorm[i][j]
    img = cv2.filter2D(img,-1,GN)
    cv2.imshow("Gaussian Blur",img)

def SobelX():
    img = cv2.imread('Chihiro.jpg',0)
    G = [[(-1,-1),(0,-1),(1,-1)],[(-1,0),(0,0),(1,0)],[(-1,1),(0,1),(1,1)]]
    GN = np.empty((3,3))
    Gnorm = [(0.045,0.122,0.045),(0.122,0.332,0.122),(0.045,0.122,0.045)]
    sigma = 0.9
    for i in range(0,3):
        for j in range(0,3):
            GN[i][j] = math.exp(-1* (G[i][j][0]*G[i][j][0] + G[i][j][1]*G[i][j][1])/2*sigma*sigma) / 2*math.pi*sigma*sigma*Gnorm[i][j]
    img = cv2.filter2D(img,-1,GN)
    SX = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    img = cv2.filter2D(img,-1,SX)
    cv2.imshow("SobelX",img)
    cv2.waitKey (0)

def SobelY():
    img = cv2.imread('Chihiro.jpg',0)
    G = [[(-1,-1),(0,-1),(1,-1)],[(-1,0),(0,0),(1,0)],[(-1,1),(0,1),(1,1)]]
    GN = np.empty((3,3))
    Gnorm = [(0.045,0.122,0.045),(0.122,0.332,0.122),(0.045,0.122,0.045)]
    sigma = 0.9
    for i in range(0,3):
        for j in range(0,3):
            GN[i][j] = math.exp(-1* (G[i][j][0]*G[i][j][0] + G[i][j][1]*G[i][j][1])/2*sigma*sigma) / 2*math.pi*sigma*sigma*Gnorm[i][j]
    img = cv2.filter2D(img,-1,GN)
    SY = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    img = cv2.filter2D(img,-1,SY)
    cv2.imshow("SobelY",img)
    cv2.waitKey (0)

def Magnitude():
    img = cv2.imread('Chihiro.jpg',0)
    G = [[(-1,-1),(0,-1),(1,-1)],[(-1,0),(0,0),(1,0)],[(-1,1),(0,1),(1,1)]]
    GN = np.empty((3,3))
    Gnorm = [(0.045,0.122,0.045),(0.122,0.332,0.122),(0.045,0.122,0.045)]
    sigma = 0.9
    for i in range(0,3):
        for j in range(0,3):
            GN[i][j] = math.exp(-1* (G[i][j][0]*G[i][j][0] + G[i][j][1]*G[i][j][1])/2*sigma*sigma) / 2*math.pi*sigma*sigma*Gnorm[i][j]
    SX = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    SY = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
    imgX = cv2.filter2D(img,-1,SX)
    imgY = cv2.filter2D(img,-1,SY)

    for i in range(len(imgX)):
        for j in range(len(imgX[i])):
            img[i][j] = np.sqrt(abs(imgX[i][j]**2 + imgY[i][j]**2))

    cv2.imshow("Magnitude",img)
    cv2.waitKey (0)
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(339, 456)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 50, 251, 321))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(30, 40, 181, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Gasussian_Blau)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 110, 181, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(SobelX)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 180, 181, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(SobelY)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 250, 181, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(Magnitude)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(70, 380, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(180, 380, 93, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HW - Q3"))
        self.groupBox.setTitle(_translate("MainWindow", "3. Edge Detection"))
        self.pushButton.setText(_translate("MainWindow", "3.1 Gaussian Blar"))
        self.pushButton_2.setText(_translate("MainWindow", "3.2 Sobel X"))
        self.pushButton_3.setText(_translate("MainWindow", "3.2 Sobel Y"))
        self.pushButton_4.setText(_translate("MainWindow", "3.4 Magnitude"))
        self.pushButton_5.setText(_translate("MainWindow", "OK"))
        self.pushButton_6.setText(_translate("MainWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

