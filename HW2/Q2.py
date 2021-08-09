# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

img_path = './Datasets/Q2_Image/'    
distortion_matrix = None
intrinsic_matrix = None
rotation_vec = None
translation_vec = None

def find_corners():
    for i in range(1,16):
        # read img
        img = cv2.imread(img_path + str(i) + '.bmp')
        # resize img
        #img2 = img
        img2 = cv2.resize(img,(1300,1000))
        # 轉成灰階圖
        img3 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        #找尋角點，找到座標放 corners_arrays
        find_it, corners_array = cv2.findChessboardCorners(img3,(11,8),None)

        if find_it == True:
            # 停止優化尋找標準
            # cv2.TERM_CRITERIA_EPS 迭代到最大次數停止，此處定 30
            # cv2.TERM_CRITERIA_MAX_ITER 角點位置變化的最小值已經達到最小時停止，此處定 0.001
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.0001)
            #優化尋找(圖片, 輸入角點陣列, 搜尋區域大小, winSize(-1,-1)是忽略, 停止優化標準)
            corners_array2 = cv2.cornerSubPix(img3, corners_array, (15,15), (-1,-1), criteria)
            # Draw corners
            img4 = cv2.drawChessboardCorners(img2, (11,8), corners_array2, find_it)
            cv2.imshow(str(i) + '.bmp',img4)
        
    
def find_intrinsic_matrix_and_distortion_matrix():
    global intrinsic_matrix, distortion_matrix, rotation_vec, translation_vec
    # 3d point in real world space
    objpoints = [] 
    # 2d points in image plane.
    imgpoints = [] 
    
    for i in range(1,16):
        # 格子有 9*12 個，角點有 8*11 個
        # objp 大小是 88*3，有 88 個[0,0,0]
        objp = np.zeros((8*11, 3), np.float32)
        # assign objp value
        objp[:,:2] = np.mgrid[0:11,0:8].T.reshape(-1,2)

        # read img
        img = cv2.imread('./Datasets/Q2_Image/' + str(i) + '.bmp')
        # 轉成灰階圖
        img3 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #找尋角點，找到座標放 corners_arrays
        find_it, corners_array = cv2.findChessboardCorners(img3,(11,8),None)

        if find_it == True:
            # 將 objp 加到 objpoints 內
            objpoints.append(objp)
            # 將 corners_array 加到 imgpoints 內
            imgpoints.append(corners_array)
        
    # let it see like demical, not science notation
    np.set_printoptions(suppress=True, precision=8)
    # find matrix  
    ret, intrinsic_matrix, distortion_matrix, rotation_vec, translation_vec = cv2.calibrateCamera(objpoints, imgpoints, img3.shape[::-1],None,None)
    #print("ret: ", ret)
    print("intrinsic matrix: \n", intrinsic_matrix)
    print("distortion matrix : \n", distortion_matrix[0])
    #print("rvecs: ", rotation_vec)
    #print("tvecs: ", translation_vec)
    
def find_extrinsic_matrix(index):
    #input index range is 1~15, array index is 0~14
    index = index - 1
    # 宣告 extrinsic_matrix 大小
    extrinsic_matrix = np.zeros((3,4), np.float32)
    # 將 rotation vec 轉成 tuple 型態
    rotation_tuple = tuple(rotation_vec[index].reshape(1, -1)[0])
    # 算出 rotation matrix
    rotation_mtx = cv2.Rodrigues(rotation_tuple)
    # 將 rotation matrix 塞入 extrinsic_matrix
    extrinsic_matrix[:,:-1] = rotation_mtx[0]
    # 將 translation matrix 塞入 extrinsic_matrix
    extrinsic_matrix[:,3] = translation_vec[index].T
    print("extrinsic_matrix: \n", extrinsic_matrix)

class Ui_MainWindow(object):
    def send_find(self, MainWindow):
        print(int(self.comboBox.currentText()),'.bmp')
        find_extrinsic_matrix(int(self.comboBox.currentText()))
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 268)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 30, 461, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 40, 111, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(find_corners)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 90, 111, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(find_intrinsic_matrix_and_distortion_matrix)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_7.setGeometry(QtCore.QRect(50, 140, 111, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(find_intrinsic_matrix_and_distortion_matrix)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(210, 40, 201, 141))
        self.groupBox_3.setObjectName("groupBox_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox.setGeometry(QtCore.QRect(30, 50, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 81, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_8.setGeometry(QtCore.QRect(50, 90, 111, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.send_find)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Q2"))
        self.groupBox_2.setTitle(_translate("MainWindow", "2. Calibration"))
        self.pushButton_3.setText(_translate("MainWindow", "2.1 Find Corners"))
        self.pushButton_4.setText(_translate("MainWindow", "2.2 Find Intrinsic"))
        self.pushButton_7.setText(_translate("MainWindow", "2.4 Find Distortion"))
        self.groupBox_3.setTitle(_translate("MainWindow", "2.3 Extrinsic"))
        self.comboBox.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "4"))
        self.comboBox.setItemText(4, _translate("MainWindow", "5"))
        self.comboBox.setItemText(5, _translate("MainWindow", "6"))
        self.comboBox.setItemText(6, _translate("MainWindow", "7"))
        self.comboBox.setItemText(7, _translate("MainWindow", "8"))
        self.comboBox.setItemText(8, _translate("MainWindow", "9"))
        self.comboBox.setItemText(9, _translate("MainWindow", "10"))
        self.comboBox.setItemText(10, _translate("MainWindow", "11"))
        self.comboBox.setItemText(11, _translate("MainWindow", "12"))
        self.comboBox.setItemText(12, _translate("MainWindow", "13"))
        self.comboBox.setItemText(13, _translate("MainWindow", "14"))
        self.comboBox.setItemText(14, _translate("MainWindow", "15"))
        self.label_3.setText(_translate("MainWindow", "Select Image"))
        self.pushButton_8.setText(_translate("MainWindow", "2.3 Find Extrinsic"))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()