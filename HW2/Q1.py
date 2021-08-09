# -*- coding: utf-8 -*-
import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

img_path = './Datasets/Q1_Image/'


class Ui_MainWindow(object):

    def count_func(self, MainWindow):
        def count_contour(imgname):
            # 原始圖片
            img  = cv2.imread(img_path + imgname)
            # 轉灰階圖
            img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
            # 做GaussianBlur
            img3 = cv2.GaussianBlur(img2,(9,9),0)
            # 轉成 binary 形式
            img4 = cv2.threshold(img3,127,255,cv2.THRESH_BINARY)
            # 讓邊界更精準
            img5 = cv2.Canny(img4[1],150,250)
            # contour detection
            contours, hierarchy = cv2.findContours(img5, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            nf_contours = int(len(contours)/2)
            print(nf_contours)
            return nf_contours
        
        _translate = QtCore.QCoreApplication.translate
        temp = 0
        temp = count_contour("coin01.jpg")
        self.label.setText(_translate("MainWindow", "Threr are " + str(temp) + " conis in coin01.jpg"))
        temp = count_contour("coin02.jpg")
        self.label_2.setText(_translate("MainWindow", "Threr are " + str(temp) + " conis in coin02.jpg"))
        count_contour("coin03.jpg")
        cv2.waitKey(0)
    
    def draw_func(self, MainWindow):
        def draw_contour(imgname):
            # 原始圖片
            img  = cv2.imread(img_path + imgname)
            # 轉灰階圖
            img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
            # 做GaussianBlur
            img3 = cv2.GaussianBlur(img2,(11,11),0)
            # 轉成 binary 形式
            img4 = cv2.threshold(img3,128,255,cv2.THRESH_BINARY)
            # 讓邊界更精準
            img5 = cv2.Canny(img4[1],150,250)
            # contour detection
            contours, hierarchy = cv2.findContours(img5, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # draw contour
            img6 = cv2.drawContours(img, contours, -1, (0, 0, 255), 2)
            cv2.imshow(imgname,img6)
            
        draw_contour("coin01.jpg")
        draw_contour("coin02.jpg")
        draw_contour("coin03.jpg")
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(259, 305)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 231, 261))
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(50, 50, 111, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.draw_func)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 110, 111, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton.clicked.connect(self.count_func)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 170, 161, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 210, 161, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Q1"))
        self.groupBox.setTitle(_translate("MainWindow", "1. Find Contour"))
        self.pushButton.setText(_translate("MainWindow", "1.1 Draw Contour"))
        self.pushButton_2.setText(_translate("MainWindow", "1.2 Count Coins"))
        self.label.setText(_translate("MainWindow", "Threr are __ conis in coin01.jpg"))
        self.label_2.setText(_translate("MainWindow", "Threr are __ conis in coin02.jpg"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()