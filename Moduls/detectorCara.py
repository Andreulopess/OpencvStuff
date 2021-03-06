import cv2
import numpy as np

faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


#   Deteccio de cara, si troba cara la requadra amb en quadrat verd
def facedetect(foto):  # Se pasa la foto deseada
    faces = faceClassif.detectMultiScale(foto,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    for (x, y, w, h) in faces:
        cv2.rectangle(foto, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 255, 0), 1)


#   Deteccio de cara, si troba cara la tapa amb en quadrat negre
def facecover(foto):  # Se pasa la foto deseada
    faces = faceClassif.detectMultiScale(foto,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    try:
        for (x, y, w, h) in faces:
            cv2.rectangle(foto, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 0, 0), -1)
    except:
        print("No se han encontrado caras")


def facecircle(image):
    faces = faceClassif.detectMultiScale(image,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))

    for (x, y, w, h) in faces:
        center_coordinates = x + w // 2, y + h // 2
        radius = w // 2  # or can be h / 2 or can be anything based on your requirements
        #cv2.circle(foto, center_coordinates, radius, (0, 0, 100), 0)



    mask = np.zeros(image.shape, dtype=np.uint8)
    cv2.circle(mask, center_coordinates, radius, (255, 255, 255), -1)

    # Bitwise-and for ROI
    ROI = cv2.bitwise_and(image, mask)

    # Crop mask and turn background white
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    cv2.imshow('mask', mask)
    x, y, w, h = cv2.boundingRect(mask)
    result = ROI[y:y + h, x:x + w]
    mask = mask[y:y + h, x:x + w]
    result[mask == 0] = (255, 255, 255)
    return result