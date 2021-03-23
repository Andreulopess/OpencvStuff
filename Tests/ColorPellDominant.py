import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt
from Moduls import detectorCara as dc




image = cv2.imread('Imatges/t1.png')
image = imutils.resize(image,width=800)
cv2.imshow('inicial', image)
result= dc.facecircle(image)


ORANGE_MIN = np.array([5, 50, 50],np.uint8)
ORANGE_MAX = np.array([15, 255, 255],np.uint8)

image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
hsv_img = cv2.cvtColor(result,cv2.COLOR_BGR2HSV)
bin = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
cv2.imshow('output2.jpg', bin)

frame_threshed = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)


data = np.reshape(result, (-1, 3))
print(data.shape)
data = np.float32(data)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)

print('Dominant color is: bgr({})'.format(centers[0].astype(np.int32)))

color = ('b','g','r')

for i, c in enumerate(color):
    hist = cv2.calcHist([result], [i], None, [256], [0, 256])
    plt.plot(hist, color = c)
    plt.xlim([0,256])
    plt.ylim([0,300])
plt.show()


hist2 = cv2.calcHist([bin], [0], None, [256], [0, 256])
plt.plot(hist2, color='gray' )
plt.ylim([0, 350])
plt.title("Foto cara")
plt.xlabel('intensidad de iluminacion')
plt.ylabel('cantidad de pixeles')
plt.show()


hist3 = cv2.calcHist([image], [0], None, [256], [0, 256])
plt.plot(hist3, color='gray' )
plt.title("Foto grossa")
plt.xlabel('intensidad de iluminacion')
plt.ylabel('cantidad de pixeles')
plt.ylim([0, 10000])
plt.show()






#cv2.imshow('result', result)
cv2.waitKey(0)