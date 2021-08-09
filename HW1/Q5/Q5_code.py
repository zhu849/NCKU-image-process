# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Input, Dense, Dropout, Activation, Flatten
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import Convolution2D, MaxPooling2D
import matplotlib.pyplot as plt
import pandas as pd
%matplotlib inline

#define parameter
nb_class = 10
batch_size = 128
epoch = 50
learning_rate = 0.01
decay = learning_rate / epoch
optimizer = 'SGD'

class_name = {
    0: 'airplane',
    1: 'automobile',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck',
}

def plot_acc_loss(h, epoch):
    acc, loss, val_acc, val_loss = h.history['acc'], h.history['loss'], h.history['val_acc'], h.history['val_loss']
    plt.figure(figsize=(15, 4))
    plt.subplot(121)
    for i in range(len(acc)):
      acc[i] = acc[i] * 100
      val_acc[i] = val_acc[i] * 100
      
    plt.plot(range(epoch), acc, label='Train')
    plt.plot(range(epoch), val_acc, label='Test')
    plt.xlabel('# of times')
    plt.ylabel('%')
    plt.legend()
    plt.title('Accuracy', size=15)
    plt.grid(True)

    plt.subplot(122)
    plt.plot(range(epoch), loss, label='Train')
    plt.plot(range(epoch), val_loss, label='Test')
    plt.xlabel('# of times')
    plt.legend()
    plt.title('Loss', size=15)
    plt.grid(True)
    plt.show()
    
def train_dataset():
    # Loading cidar10 dataset
    # x is image information and y is label number
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    # reshape dimension with y*1 to 1*y(flatten)
    y_train = y_train.reshape(y_train.shape[0])
    y_test = y_test.reshape(y_test.shape[0])
    # short record format, will loss some precision but is better to stored  
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    x_train /= 255
    x_test /= 255
    # let label number to classifying to 10 catergory
    y_train = to_categorical(y_train, nb_class)
    y_test = to_categorical(y_test, nb_class)


    x = Input(shape=(32, 32, 3))
    y = x
    y = Convolution2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=128, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=128, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=256, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=256, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Flatten()(y)
    y = Dense(units=128, activation='relu', kernel_initializer='he_normal')(y)
    y = Dropout(0.5)(y)
    y = Dense(units=nb_class, activation='softmax', kernel_initializer='he_normal')(y)

    VGGmodel = Model(inputs=x, outputs=y, name='modelVGG16')
    #VGGmodel.summary()

    # define parameters
    sgd = optimizers.SGD(lr=learning_rate, momentum=0.9, decay=decay, nesterov=False)
    loss_function = 'categorical_crossentropy'

    # start train
    VGGmodel.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['acc'])
    h = VGGmodel.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epoch, validation_data=(x_test, y_test), shuffle=True)
    #VGGmodel.save('VGGmodel.h5')
    VGGmodel.save('saved_model/my_model') 
    plot_acc_loss(h, epoch)
    
def show_train_image():
    # Loading cidar10 dataset
    # x is image information and y is label number
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    # reshape dimension with y*1 to 1*y(flatten)
    y_train = y_train.reshape(y_train.shape[0])
    y_test = y_test.reshape(y_test.shape[0])
    # short record format, will loss some precision but is better to stored  
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    x_train /= 255
    x_test /= 255
    # let label number to classifying to 10 catergory
    y_train = to_categorical(y_train, nb_class)
    y_test = to_categorical(y_test, nb_class)
    rand_id = np.random.choice(range(10000), size=10)
    x_pred = np.array([x_test[i] for i in rand_id])

    y_true = [y_test[i] for i in rand_id]
    y_true = np.argmax(y_true, axis=1)
    y_true = [class_name[name] for name in y_true]
    
    plt.figure(figsize=(15, 8))
    for i in range(10):
        plt.subplot(2, 5, i + 1)
        plt.imshow(x_pred[i].reshape(32, 32, 3), cmap='gray')
        plt.title('Label: %s \n' % (y_true[i]), size=15)
    plt.show()
    
def show_hyperparameter():
    print('Hyperparameters:')
    print('batch_size = 128')
    print('learning_rate = 0.01')
    print('optimizer = SGD')
    print('epoch = 50')
    
def show_modelstructure():
    x = Input(shape=(32, 32, 3))
    y = x
    y = Convolution2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=128, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=128, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=256, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=256, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = Convolution2D(filters=512, kernel_size=3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal')(y)
    y = MaxPooling2D(pool_size=2, strides=2, padding='valid')(y)

    y = Flatten()(y)
    y = Dense(units=128, activation='relu', kernel_initializer='he_normal')(y)
    y = Dropout(0.5)(y)
    y = Dense(units=nb_class, activation='softmax', kernel_initializer='he_normal')(y)

    VGGmodel = Model(inputs=x, outputs=y, name='modelVGG16')
    VGGmodel.summary()
    VGGmodel.get_config()
    
def show_accuracy():
    img = cv2.imread('result.JPG')
    img = cv2.resize(img,(1000,450))
    cv2.imshow('Accuracy & Loss',img)
    
def test_image(index):
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    y_train = y_train.reshape(y_train.shape[0])
    y_test = y_test.reshape(y_test.shape[0])
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    y_train = to_categorical(y_train, nb_class)
    y_test = to_categorical(y_test, nb_class)
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    y_train = y_train.reshape(y_train.shape[0])
    y_test = y_test.reshape(y_test.shape[0])
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    y_train = to_categorical(y_train, nb_class)
    y_test = to_categorical(y_test, nb_class)

    mymodel = load_model('VGGmodel.h5')
    x_pred = np.array(x_test[index])
    plt.imshow(x_pred)

    test = np.reshape(x_test[index],(1,32,32,3))
    y_pred = mymodel.predict(test)
    pred_name = np.argmax(y_pred, axis=1)
    print("Predict： " + class_name[int(pred_name)])

    plt.figure(figsize=(10,6))
    y_pred = np.reshape(y_pred,(10))

    label_name = ['airplane', 'automobile','bird','cat','deer','dog','frog','horse','ship','truck',]
    plt.bar(label_name, width = 0.35, height=y_pred)
    plt.show()

class Ui_MainWindow(object):
    def buttonclick(self):
        test_index= int(self.spinBox.value())
        test_image(test_index)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 270)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 131, 21))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(show_train_image)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 70, 131, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(show_hyperparameter)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 110, 131, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(show_modelstructure)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 150, 131, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(show_accuracy)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setRange(0, 10000)
        self.spinBox.setGeometry(QtCore.QRect(30, 190, 121, 22))
        self.spinBox.setObjectName("spinBox")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(20, 220, 131, 21))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.buttonclick)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Q5"))
        self.pushButton.setText(_translate("MainWindow", "1.Show Train Images"))
        self.pushButton_2.setText(_translate("MainWindow", "2. Show Hyperparameters"))
        self.pushButton_3.setText(_translate("MainWindow", "3.Show Model Structure"))
        self.pushButton_4.setText(_translate("MainWindow", "4.Show Accuracy"))
        self.pushButton_5.setText(_translate("MainWindow", "5.Test"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
