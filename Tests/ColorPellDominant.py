import cv2
import numpy as np
from Moduls import detectorCara as dc




image = cv2.imread('Imatges/t1.png')
cv2.imshow('inicial', image)
result= dc.facecircle(image)


ORANGE_MIN = np.array([5, 50, 50],np.uint8)
ORANGE_MAX = np.array([15, 255, 255],np.uint8)

hsv_img = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)

frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
cv2.imshow('output2.jpg', result)
#cv2.imshow('result', result)
cv2.waitKey(0)