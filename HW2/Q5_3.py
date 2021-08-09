import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

re_x = 112
re_y = 224

cat_val = [0,0]
dog_val = [0,0]

mymodel = load_model("resnet_best.h5")
np.set_printoptions(suppress=True, precision=8)
index = random.randrange(8000, 12499, 1)
img = cv2.imread('%d.jpg' % index)
# original image
img2 = cv2.resize(img, (224, 224))
img2.astype(np.float32)
img3 = img2.reshape(1,224,224,3)
val = mymodel.predict(img3)
cat_val[0] = (100 - val*100)
dog_val[0] = (val*100)
cv2.imshow('test',img2)

img4 = cv2.resize(img, (re_x, re_y))
img4.astype(np.float32)
img5 = img4.reshape(1,re_x,re_y,3)
val = mymodel.predict(img5)
cat_val[1] = (100 - val*100)
dog_val[1] = (val*100)
cv2.imshow('test2',img4)
print("Original: Cat ",cat_val[0][0][0],"%, Dog ",dog_val[0][0][0], "%")
print("After: Cat ",cat_val[1][0][0],"%, Dog ",dog_val[1][0][0], "%")
cv2.waitKey(0)