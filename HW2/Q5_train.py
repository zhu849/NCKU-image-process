import random
import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization, merge, Input
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, AveragePooling2D, GlobalAveragePooling2D
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.utils import np_utils
from keras.models import model_from_json,load_model, Model
from keras import backend as K
from keras.preprocessing import image
from keras.optimizers import SGD
from keras.utils.data_utils import get_file
from keras import layers
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import preprocess_input
from datetime import datetime

%matplotlib inline

# random print 16 imgs in terminal with plt 
def random_print():
    x, y = train_generator.next()

    plt.figure(figsize=(16, 8))
    for i, (img, label) in enumerate(zip(x, y)):
        plt.subplot(3, 6, i+1)
        if label == 1:
            plt.title('dog')
        else:
            plt.title('cat')
            plt.axis('off')
            plt.imshow(img, interpolation="nearest")

# 定義一個 identity block，輸入和輸出維度相同，可串聯，用於加深網路
def identity_block(input_tensor, kernel_size, filters, stage, block):
    """The identity block is the block that has no conv layer at shortcut.
    # Arguments
        input_tensor: input tensor
        kernel_size: defualt 3, the kernel size of middle conv layer at main path
        filters: list of integers, the filterss of 3 conv layer at main path
        stage: integer, current stage label, used for generating layer names
        block: 'a','b'..., current block label, used for generating layer names
    # Returns
        Output tensor for the block.
    """
    filters1, filters2, filters3 = filters
    if K.image_data_format() == 'channels_last':
        bn_axis = 3
    else:
        bn_axis = 1

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    # default stride = 1
    x = Convolution2D(filters1, (1, 1), name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Convolution2D(filters2, kernel_size, padding='same', name=conv_name_base + '2b')(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)

    x = Convolution2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2c')(x)

    x = layers.add([x, input_tensor])
    x = Activation('relu')(x)
    return x

# 定義一個會重複的捲積結構 - conv Block，輸入和輸出維度不同，不可串聯，用於改變網路維度
def conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2, 2)):
    """conv_block is the block that has a conv layer at shortcut
    # Arguments
        input_tensor: input tensor
        kernel_size: defualt 3, the kernel size of middle conv layer at main path
        filters: list of integers, the filterss of 3 conv layer at main path
        stage: integer, current stage label, used for generating layer names
        block: 'a','b'..., current block label, used for generating layer names
    # Returns
        Output tensor for the block.
    Note that from stage 3, the first conv layer at main path is with strides=(2,2)
    And the shortcut should have strides=(2,2) as well
    """
    # 分別解出各個 filter 的值
    filters1, filters2, filters3 = filters
    
    # 選擇捲積使用的軸
    if K.image_data_format() == 'channels_last':
        bn_axis = 3
    else:
        bn_axis = 1
        
    # 為新定義的層統一名稱
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Convolution2D(filters1, (1, 1), strides=strides, name=conv_name_base + '2a')(input_tensor)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2a')(x)
    x = Activation('relu')(x)

    x = Convolution2D(filters2, kernel_size, padding='same',  name=conv_name_base + '2b')(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2b')(x)
    x = Activation('relu')(x)
    
    # 經歷兩層後將捲積和 short cut 結合後再輸出
    x = Convolution2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2c')(x)
    
    # 捷徑路線
    shortcut = Convolution2D(filters3, (1, 1), strides=strides, name=conv_name_base + '1')(input_tensor)
    shortcut = BatchNormalization(axis=bn_axis, name=bn_name_base + '1')(shortcut)
    
    # H(x) = F(x) + shortcut
    x = layers.add([x, shortcut])
    x = Activation('relu')(x)
    return x


if __name__ == "__main__":
    # 定義要處理影像的大小參數
    image_width = 224
    image_height = 224
    image_size = (image_width, image_height)

    # 讀取資料集 && 驗證集
    train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    train_generator = train_datagen.flow_from_directory(
          './Train',  # this is the target directory
          target_size=image_size,  # all images will be resized to 224x224
          batch_size=4, # 一次讀16張
          class_mode='binary') # 格式是二進位檔案

    validation_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    validation_generator = validation_datagen.flow_from_directory(
          './Validation',  # this is the target directory
          target_size=image_size,  # all images will be resized to 224x224
          batch_size=4,
          class_mode='binary')

    #這subfunc可以確認是否正確讀到資料集
    #random_print()

    ### 利用 conv Block 和 identity_block 建構 resNet50 架構 ###
    ## conv1
    # 定義 input shape = (None, 224, 224, 3)
    img_input = Input(shape=(image_width, image_height, 3)) # Input() is used to instantiate a Keras tensor.
    af_padding = ZeroPadding2D((3, 3))(img_input) # Zero-padding layer for 2D input , size will be (None, 230, 230, 3)
    # padding 的目的應該是因為用 7*7 去做捲積?
    # 因為 strides = 2, 所以 conv1 size = (None, 115, 115, 64) , format:(rows, cols, filters)
    conv1 = Convolution2D(filters=64, kernel_size=(7,7), padding="same", strides=(2,2), name='conv1', data_format='channels_last')(af_padding)

    # 每次捲積後都需要做一次 Batch Normorlization, 做完後大小相同，僅是將內容值平滑化, axis = 3 表示用第三個當作 "軸" 做操作
    BN_conv1 = BatchNormalization(axis=3, name='bn_conv1')(conv1)
    #BN_conv1 = conv1
    # 將輸入透過 relu 函數轉換, 輸出是相同 size 
    relu_conv1 = Activation('relu')(BN_conv1)
    
    ## stage2
    # 從3*3方格內找到最大值代表一格，且每次 Stride 為2，所以 col & row 變成一半，size = (Noen, 58, 58, 64)
    maxPool_conv1 = MaxPooling2D  (pool_size=(3, 3), strides=(2, 2), padding="same")(relu_conv1)
    # conv2 return size = (None, 29, 29, 256)
    conv2_a = conv_block(maxPool_conv1, 3, [64, 64, 256], stage=2, block='a')
    conv2_b = identity_block(conv2_a, 3, [64, 64, 256], stage=2, block='b')
    conv2_c = identity_block(conv2_b, 3, [64, 64, 256], stage=2, block='c')    
    
    ## stage3
    # conv3 return size = (None, 15, 15, 512)
    conv3_a = conv_block    (conv2_c, 3, [128, 128, 512], stage=3, block='a')
    conv3_b = identity_block(conv3_a, 3, [128, 128, 512], stage=3, block='b')
    conv3_c = identity_block(conv3_b, 3, [128, 128, 512], stage=3, block='c')
    conv3_d = identity_block(conv3_c, 3, [128, 128, 512], stage=3, block='d')
    
    ## stage4
    # conv4 return size = (None, 8, 8, 1024)
    conv4_a = conv_block    (conv3_d, 3, [256, 256, 1024], stage=4, block='a')
    conv4_b = identity_block(conv4_a, 3, [256, 256, 1024], stage=4, block='b')
    conv4_c = identity_block(conv4_b, 3, [256, 256, 1024], stage=4, block='c')
    conv4_d = identity_block(conv4_c, 3, [256, 256, 1024], stage=4, block='d')
    conv4_e = identity_block(conv4_d, 3, [256, 256, 1024], stage=4, block='e')
    conv4_f = identity_block(conv4_e, 3, [256, 256, 1024], stage=4, block='f')
   
    ## stage5
    # conv5 return size = (None, 4, 4, 2048)
    conv5_a = conv_block    (conv4_f, 3, [512, 512, 2048], stage=5, block='a')
    conv5_b = identity_block(conv5_a, 3, [512, 512, 2048], stage=5, block='b')
    conv5_c = identity_block(conv5_b, 3, [512, 512, 2048], stage=5, block='c')
    
    #construct model
    base_model = Model(img_input, conv5_c)
    
    
    TF_WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.2/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'
    weights_path = get_file('resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                        TF_WEIGHTS_PATH_NO_TOP,
                        cache_subdir='models',
                        md5_hash='a268eb855778b3df3c7506639542a6af')
    base_model.load_weights(weights_path)
    
    
    # add top layer to ResNet-50
    x = AveragePooling2D((7, 7), name='avg_pool', padding = "same")(base_model.output)
    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = Dense(1, activation='sigmoid', name='output')(x)

    model = Model(base_model.input, x)
    #model.summary()
    
    top_num = 4
    for layer in model.layers[:-top_num]:
        layer.trainable = False

    for layer in model.layers[-top_num:]:
        layer.trainable = True

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    best_model = ModelCheckpoint("resnet_best.h5", monitor='val_accuracy', verbose=0, save_best_only=True)
    
    model.fit_generator(
        train_generator,
        epochs=8,
        validation_data=validation_generator,
        callbacks=[best_model,TensorBoard(log_dir='./logs', histogram_freq=1,update_freq=1000)])
   
    with open('resnet.json', 'w') as f:
        f.write(model.to_json())
