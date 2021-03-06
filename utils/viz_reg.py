from train import IndexFingerDataset
from train import get_index_finger_predictor
import numpy as np
import torch
import cv2

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)

predictor = get_index_finger_predictor()
testset = IndexFingerDataset('data/X_test.npy', 'data/Y_test.npy')
testloader = iter(torch.utils.data.DataLoader(testset, batch_size=1))

image_width = 160
image_height = 90

while True:

    data = next(testloader)
    im = data['image'].numpy().reshape(image_height, image_width, 3).astype(np.uint8)
    label = tuple(np.ravel(data['label'].numpy()))

    px, py = label
    position = (int((px + 0.5) * image_width), int((py + 0.5) * image_height))
    cv2.circle(im, position, 3, GREEN, thickness=-1)

    x, y = predictor(im)
    cv2.circle(im, (x, y), 3, BLUE, thickness=-1)

    cv2.imshow('frame', im)
    if cv2.waitKey(500) & 0xFF == ord('q'):
        break
