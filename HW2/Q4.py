# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

img_path = './Datasets/Q4_Image/'
img3 = None
img4 = None

def calu_depth(event,x,y,flags,param):
    global img3, img4
    if event == cv2.EVENT_LBUTTONDOWN:
        img4 = img3.copy()
        cv2.putText(img4, 'Disparity: ' + str(img3[y][x]) + ' pixels', (980,850), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        depth = int((178*2826)//(img3[y][x]+123))
        cv2.putText(img4, 'Depth: ' + str(depth) + ' mm', (980,880), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

def stereo():
    global img3, img4
    imgL = cv2.imread(img_path + 'imgL.png', 0)
    imgL = cv2.resize(imgL,(1410,960))
    imgL = cv2.normalize(imgL, imgL, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    imgR = cv2.imread(img_path + 'imgR.png', 0)
    imgR = cv2.resize(imgR,(1410,960))
    imgR = cv2.normalize(imgR, imgR, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # will generate 16 bits, if direct store will store in shape 8 bit and 3 channels
    # need compute 16 bits to 8 bits
    stereo = cv2.StereoBM_create(numDisparities = 128, blockSize = 23)
    disparity = stereo.compute(imgL,imgR)
    
    disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC3)
    #img2 = disparity
    img2 = cv2.resize(disparity,(1410,960))
    img3 = np.asarray(img2)
    img4 = img3.copy()
    cv2.namedWindow('Disparity')
    cv2.setMouseCallback("Disparity", calu_depth)

    while(1):
        cv2.imshow('Disparity', img4)
        op = cv2.waitKey(20) & 0xFF
        if op == 27:
            break

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(277, 171)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 20, 221, 111))
        self.groupBox_5.setObjectName("groupBox_5")
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_10.setGeometry(QtCore.QRect(40, 50, 141, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.clicked.connect(stereo)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Q4"))
        self.groupBox_5.setTitle(_translate("MainWindow", "4. Stereo Disparity Map"))
        self.pushButton_10.setText(_translate("MainWindow", "4.1 Stereo Disparity Map"))
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()