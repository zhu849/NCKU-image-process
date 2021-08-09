tensorboard_batch.jpg 紀錄的是最佳那次 epoch 的趨勢圖
tensorboard_epoch.jpg 紀錄的是8次 epoch 的趨勢圖
train_224224.jpg 紀錄的是用 224*224 大小去 training 的 checkpoint
train_random.jpg 紀錄的是用不同大小去 training 的 checkpoint

訓練集、驗證集、測試集分類方式：
Train:
	Cat:0-7999 = 8000
	Dog:0-7999 = 8000
Vaildation:
	Cat:10000-12499 = 2500
	Dog:8000-10000,12000-12499 = 2500
Test:
	Cat:8000-10000 = 2000
	Dog:10001-11999 = 2000