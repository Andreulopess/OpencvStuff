import cv2
from MansXarxa.models import DetectorPersona as dp
from MansXarxa import demo2 as hand

from MansXarxa.yolo import YOLO

# https://pysource.com/2019/06/27/yolo-object-detection-using-opencv-with-python/
yolo = YOLO("MansXarxa/models/cross-hands.cfg", "MansXarxa/models/cross-hands.weights", ["hand"])

#   Carregar foto

img = cv2.imread("Imatges/ErwanMaAdalt.png")
img2 = cv2.imread("Imatges/ErweanMaAbix.png")

# Aillar persona (Detector persona)
# ALERTA AMB DIRECCIÓ DINS  Detctor persona
crop, xinicial, yinicial = dp.trobarpersona(img)

# Cercam mans
if hand.punts(crop, yolo) == -1:
    # Aqui cridariem a colorPell
    print("No s'han trobat mans a la imatge 1")
else:
    print("Hem trobat mans a foto 1")
    # Cercam mans a la nova foto i guardam punts a cx,cy
    xma, yma, wma, hma = hand.punts(crop, yolo)
    # Paràmetres per quadrat
    x1primera = xma
    y1primera = yma
    x2 = xma + wma
    y2 = yma + hma
    cx = int(x2 - wma / 2)
    cy = int(y2 - hma / 2)
    # Dibuixam rectangle
    cv2.rectangle(crop, (x1primera, y1primera), (x2, y2), (0, 255, 0), 1)
    cv2.imshow("Crop1", crop)

    #   Mostram imatge amb rectangle

# Aillar persona (Detector persona)
# ALERTA AMB DIRECCIÓ DINS  Detctor persona
crop2, lol1, lol2 = dp.trobarpersona(img2)
if hand.punts(crop2, yolo) == -1:
    # Aqui cridariem a colorPell
    print("No s'han trobat mans a la imatge 2")
else:
    print("Hem trobat mans a foto 2")
    # Cercam mans a la nova foto i guardam punts a cx,cy
    xma, yma, wma, hma = hand.punts(crop2, yolo)
    # Paràmetres per quadrat
    x1segona = xma
    y1segona = yma
    x2 = xma + wma
    y2 = yma + hma
    cx2 = int(x2 - wma / 2)
    cy2 = int(y2 - hma / 2)
    # Dibuixam rectangle
    cv2.rectangle(crop2, (x1segona, y1segona), (x2, y2), (0, 255, 0), 1)

    #   Mostram imatge amb rectangle
    cv2.imshow("Crop2", crop2)
try:
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    cv2.line(img, (xinicial + cx, yinicial + cy), (xinicial + cx2, yinicial + cy2), (0, 233, 0), 2)

except NameError:
  print("CUIDAO! Variables de posicio no definides")

# Mostram a imatge final
cv2.imshow("Final", img)

if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    exit()
