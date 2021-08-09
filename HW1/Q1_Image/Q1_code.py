# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import numpy as np

def load_image():
    img = cv2.imread('Uncle_Roger.jpg')
    img = cv2.resize(img,(600,400))
    cv2.imshow('Load',img)
    size = img.shape
    print("height:",size[0])
    print("weight:",size[1])
    
def color_separation():
    img = cv2.imread('Flower.jpg')
    img = cv2.resize(img,(600,400))
    cv2.imshow('Original',img)
    img_R = img.copy()
    img_R[:,:,0] = 0
    img_R[:,:,1] = 0
    cv2.imshow('Red',img_R)
    img_G = img.copy()
    img_G[:,:,0] = 0
    img_G[:,:,2] = 0
    cv2.imshow('Green',img_G)
    img_B = img.copy()
    img_B[:,:,1] = 0
    img_B[:,:,2] = 0
    cv2.imshow('Blue',img_B)

def flip_image():
    img = cv2.imread('Uncle_Roger.jpg')
    img = cv2.resize(img,(600,400))
    cv2.imshow('Original',img)
    img_f = cv2.flip(img,1)
    img_f = cv2.resize(img_f,(600,400))
    cv2.imshow('Result',img_f)
    
def blending_value(x):
    img = cv2.imread('Uncle_Roger.jpg')
    img_f = cv2.flip(img,1)
    img_b = cv2.addWeighted(img_f, (x/255), img, (255-x)/255, 0)
    img_b = cv2.resize(img_b,(600,400))
    cv2.imshow('Blending',img_b)
    
def blend_image():
    cv2.namedWindow('Blending')
    cv2.createTrackbar('blend','Blending',0,255, blending_value)
    cv2.setTrackbarPos('blend','Blending', 127)
    

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(290, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 221, 281))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 141, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(load_image)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 100, 141, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(color_separation)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 160, 141, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(flip_image)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 220, 141, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(blend_image)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HW - Q1"))
        self.groupBox.setTitle(_translate("MainWindow", "1. Image Processing"))
        self.pushButton.setText(_translate("MainWindow", "1.1 Load Image"))
        self.pushButton_2.setText(_translate("MainWindow", "1.2 Color Separation"))
        self.pushButton_3.setText(_translate("MainWindow", "1.3 Image Flipping"))
        self.pushButton_4.setText(_translate("MainWindow", "1.4 Blending"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
