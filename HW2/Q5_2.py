import cv2
tb_batch = cv2.imread('./Q5/tensorboard_batch.JPG')
tb_epoch = cv2.imread('./Q5/tensorboard_epoch.JPG')
cv2.imshow('tb_batch',tb_batch)
cv2.imshow('tb_epoch',tb_epoch)
cv2.waitKey(0)