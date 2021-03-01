import cv2
import numpy as np
from models import DetectorPersona as dp

imatge = cv2.imread("images/ErweanMaAbix.jpg")
print(imatge)
newcrop = dp.trobarpersona(imatge)
cv2.imshow("Resultat", newcrop)

if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    exit()