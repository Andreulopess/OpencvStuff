import cv2
from Moduls import detectorCara as dc
import imutils
from MansXarxa import demo2 as d2

imatge = cv2.imread("Imatges/Mabaix.jpg")
imatge = imutils.resize(imatge,width=800)
dc.facecover(imatge)
cv2.imshow("Resultat",imatge)
cv2.waitKey(0)
cv2.destroyAllWindows()