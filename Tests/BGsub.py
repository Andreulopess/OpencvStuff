import imutils
import numpy as np
from Moduls import detectorCara as fd
import cv2

# ---------------------DEFINICI0 DE VARIABLES----------------

maadalt = cv2.imread("Imatges/t1.png")
maabaix = cv2.imread("Imatges/T2.png")
cv2.imshow("Ex", np.hstack([maadalt, maabaix]))

# definim array
lower = np.array([0, 10, 60], dtype="uint8")
upper = np.array([20, 150, 255], dtype="uint8")

# Tapam primer cara de la persona
fd.facecover(maadalt)

# Modificar mida, troba mes punts
# Convertir a espai HSV
# Determinar els pixels que s'ajusten als arrays
frame = imutils.resize(maadalt, width=800)
converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
skinMask = cv2.inRange(converted, lower, upper)
cv2.imshow("SkinMask", skinMask)
cv2.imshow("Frame coverted", np.hstack([frame, converted]))

# Aplica erosions i dilatacions
# Empleant kernel eliptic
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
skinMask = cv2.erode(skinMask, kernel, iterations=2)
skinMask = cv2.dilate(skinMask, kernel, iterations=2)
# Desenfocar mascara per llevar renou
# Aplicar mascara al frame


skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
skinMaadalt = cv2.bitwise_and(frame, frame, mask=skinMask)
skinMaadalt = cv2.putText(skinMaadalt, 'Imatge 2', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

fd.facecover(maabaix)

frame2 = imutils.resize(maabaix, width=800)
converted = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
skinMask = cv2.inRange(converted, lower, upper)
# Aplica erosions i dilatacions
# Empleant kernel eliptic
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
skinMask = cv2.erode(skinMask, kernel, iterations=2)
skinMask = cv2.dilate(skinMask, kernel, iterations=2)
# Desenfocar mascara per llevar renou
# Aplicar mascara al frame

skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
skinMaabaix = cv2.bitwise_and(frame2, frame2, mask=skinMask)
skinMaabaix = cv2.putText(skinMaabaix, 'Imatge 1', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# show the skin in the image along with the mask

cv2.imshow("Ma adalt i abaix", np.hstack([skinMaabaix, skinMaadalt]))

cv2.imwrite("Ma_abaix.jpg", skinMaabaix)
cv2.imwrite("Ma_adalt.jpg", skinMaadalt)

if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    exit()
