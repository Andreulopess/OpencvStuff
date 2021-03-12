import cv2
import numpy as np
import imutils
from Moduls import detectorCara as dc




image = cv2.imread('Imatges/t1.png')
image = imutils.resize(image,width=800)
cv2.imshow('inicial', image)
result= dc.facecircle(image)


ORANGE_MIN = np.array([5, 50, 50],np.uint8)
ORANGE_MAX = np.array([15, 255, 255],np.uint8)

hsv_img = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)

frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
cv2.imshow('output2.jpg', result)

data = np.reshape(result, (-1, 3))
print(data.shape)
data = np.float32(data)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

print('Dominant color is: bgr({})'.format(centers[0].astype(np.int32)))

#cv2.imshow('result', result)
cv2.waitKey(0)