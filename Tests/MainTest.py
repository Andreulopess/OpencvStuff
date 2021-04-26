import cv2
from MansXarxa.models import DetectorPersona as dp
from Moduls import detectorCara as dc
from MansXarxa import demo2 as hand
import imutils

from MansXarxa.yolo import YOLO


def moviment(x_inicial, y_incial, x_final, y_final):
    if (y_incial > y_final):  # puja ma
        if (x_inicial > x_final):
            print("Direcció adalt i esquerra")
        elif (x_inicial < x_final):
            print("Direcció adalt i dreta")
    elif (y_incial < y_final):
        if (x_inicial > x_final):
            print("Direcció abaix i esquerra")
        elif (x_inicial < x_final):
            print("Direcció abaix i dreta")


# https://pysource.com/2019/06/27/yolo-object-detection-using-opencv-with-python/

yolo = YOLO("MansXarxa/models/cross-hands.cfg", "MansXarxa/models/cross-hands.weights", ["hand"])

#   Carregar foto
def busca(img,img2):
    nomFoto = str(img)

   # img = cv2.imread("Imatges/Mabaix.jpg")
    #img2 = cv2.imread("Imatges/Maadalt.jpg")


    #   Guardam centres de cara per utilitzar mes tard
    centreXImg1, centreYImg1 = dc.centresFoto(img)
    centreXImg2, centreYImg2 = dc.centresFoto(img2)

    # Aïllar persona (Detector persona)
    # ALERTA AMB DIRECCIÓ DINS  Detctor persona
    crop = img

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


    crop2 = img2
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

        cv2.line(img, (cx, cy), ( cx2, cy2), (0, 233, 0), 2)
    try:
       if (cy>centreYImg1):
            print("Per ma esquerra tenim: ")
            moviment(cx, cy, cx2, cy2)

        # img = cv2.resize(img, None, fx=0.4, fy=0.4)
        

    except NameError:
        print("CUIDAO! Variables de posició per fer linia entre mans no definides")

    # Mostram a imatge final
    #cv2.imshow("nomFoto", img)


if __name__ == '__main__':
    maadalt = cv2.imread("Imatges/t1.png")
    maabaix = cv2.imread("Imatges/t2.png")
    busca(maadalt,maabaix)



