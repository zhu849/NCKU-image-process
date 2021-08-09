# -*- coding: utf-8 -*-
import cv2
import numpy as np
from threading import Timer
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# -- global parameter -- 
img_path = './Datasets/Q3_Image/'    
distortion_matrix = None
intrinsic_matrix = None
rotation_vec = None
rotation_mtx_vec = []
translation_vec = None
af_pic = []    
counter = 0
timer = None

def find_intrinsic_matrix_and_distortion_matrix():
    global intrinsic_matrix, distortion_matrix, rotation_vec, translation_vec
    # 3d point in real world space
    objpoints = [] 
    # 2d points in image plane.
    imgpoints = [] 
    
    for i in range(1,6):
        # 格子有 9*12 個，角點有 8*11 個
        # objp 大小是 88*3，有 88 個[0,0,0]
        objp = np.zeros((8*11, 3), np.float32)
        # assign objp value
        objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)

        # read img
        img = cv2.imread(img_path + str(i) + '.bmp')
        # 轉成灰階圖
        img3 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #找尋角點，找到座標放 corners_arrays
        find_it, corners_array = cv2.findChessboardCorners(img3,(11,8),None)

        if find_it == True:
            # 將 objp 加到 objpoints 內
            objpoints.append(objp)
            # 將 corners_array 加到 imgpoints 內
            imgpoints.append(corners_array)
    # find matrix  
    ret, intrinsic_matrix, distortion_matrix, rotation_vec, translation_vec = cv2.calibrateCamera(objpoints, imgpoints, img3.shape[::-1],None,None)


def draw_picture(corners, img, index): 
    index = index - 1
    # Projects 3D points to an image plane
    corners, _ = cv2.projectPoints(corners, rotation_vec[index], translation_vec[index], intrinsic_matrix, distortion_matrix[0])
    # 去除不必要的維度
    corners = np.squeeze(corners, axis=1)
    # 將 list 內的 pair 分組
    corners = [tuple(i) for i in corners]
 
    # 轉回三原色圖
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    # 將角點和角點連接
    img = cv2.line(img, corners[0], corners[1], [0, 0, 255], 8)
    img = cv2.line(img, corners[0], corners[2], [0, 0, 255], 8)
    img = cv2.line(img, corners[0], corners[3], [0, 0, 255], 8)
    img = cv2.line(img, corners[1], corners[2], [0, 0, 255], 8)
    img = cv2.line(img, corners[1], corners[3], [0, 0, 255], 8)
    img = cv2.line(img, corners[2], corners[3], [0, 0, 255], 8)
    img = cv2.resize(img, (800, 800))
    return img

def slideshow():
    global counter, timer
    cv2.imshow('Augmented_Reality',af_pic[counter%5])
    counter = counter + 1
    timer = Timer(1, slideshow)
    timer.start()

def augmented_reality():
    find_intrinsic_matrix_and_distortion_matrix()
    #輸入金字塔座標軸
    corners = np.array([(3,3,-3), (1,1,0), (3,5,0), (5,1,0)], dtype=np.float32)
    # 計算五張圖片合成 AR 後的圖片
    for i in range(1,6):
        img = cv2.imread(img_path + str(i) + ".bmp")
        img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 合成 AR 圖片
        af_pic.append(draw_picture(corners, img2, i))
        
    slideshow()
    cv2.waitKey(0)
    timer.cancel()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(285, 175)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 20, 221, 111))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_9.setGeometry(QtCore.QRect(40, 50, 141, 23))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(augmented_reality)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Q3"))
        self.groupBox_4.setTitle(_translate("MainWindow", "3. Augmented  Reality"))
        self.pushButton_9.setText(_translate("MainWindow", "3.1 Augmented Reality"))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()