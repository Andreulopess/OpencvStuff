import cv2
from Moduls import detectorCara as dc
import imutils
import MainTest
from MansXarxa.models import DetectorPersona as dp
i1 = cv2.imread("Imatges/DuesMans.jpg")
i2 = cv2.imread("Imatges/DuesMans2.jpg")
#Per cada una cropear

i1 = imutils.resize(i1, 800)
i2 = imutils.resize(i2, 800)

i1,_,_ = dp.trobarpersona(i1)
cv2.imshow("e",i1)
'''
i1,_,_ = dp.trobarpersona(i1)
i2,_,_ = dp.trobarpersona(i2)


i1dreta,i1esquerra = dc.cropDretaEsq(i1)
i2dreta,i2esquerra = dc.cropDretaEsq(i2)

MainTest.main(i1dreta,i2dreta)
MainTest.main(i1esquerra,i2esquerra)

'''
if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    exit()
