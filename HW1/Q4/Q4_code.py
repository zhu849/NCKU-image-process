# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy
import cv2

def Transformation(deg,scale,tx,ty):
    img = cv2.imread("Parrot.png")
    cv2.imshow('Original Image',img)
    (height, weight) = img.shape[:2]
    
    T = cv2.getRotationMatrix2D((height/2,weight/2), deg, scale)
    T[0][2] = ty
    T[1][2] = tx
    res = cv2.warpAffine(img,T,(weight,height))
    cv2.imshow('Image RST',res)

class Ui_MainWindow(object):
    def buttonclick(self):
            deg = int(self.lineEdit.text())
            scale = float(self.lineEdit_2.text()) 
            tx = int(self.lineEdit_3.text()) 
            ty = int(self.lineEdit_4.text()) 
            Transformation(deg,scale,tx,ty)
            
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(314, 331)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 271, 221))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 58, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(200, 40, 58, 15))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(80, 40, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 58, 15))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 80, 113, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 58, 15))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 120, 113, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(200, 120, 58, 15))
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 160, 58, 15))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(200, 160, 58, 15))
        self.label_6.setObjectName("label_6")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 160, 113, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 260, 231, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.buttonclick)
        print(self.lineEdit.text)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HW - Q4"))
        self.groupBox.setTitle(_translate("MainWindow", "4. Transformation"))
        self.label.setText(_translate("MainWindow", "Rotation:"))
        self.label_2.setText(_translate("MainWindow", "deg"))
        self.label_3.setText(_translate("MainWindow", "Scaling:"))
        self.label_4.setText(_translate("MainWindow", "Tx:"))
        self.label_5.setText(_translate("MainWindow", "pixel"))
        self.label_7.setText(_translate("MainWindow", "Ty:"))
        self.label_6.setText(_translate("MainWindow", "pixel"))
        self.pushButton.setText(_translate("MainWindow", "4. Transformation"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()

