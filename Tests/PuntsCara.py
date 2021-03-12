import cv2
from Moduls import detectorCara as dc
import imutils
import MainTest as lolaso
i1 = cv2.imread("Imatges/Mabaix.jpg")
i2 = cv2.imread("Imatges/Maadalt.jpg")
lolaso.main(i1,i2)
if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    exit()
