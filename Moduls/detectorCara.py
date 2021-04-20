import cv2
import numpy as np

faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


#   Deteccio de cara, si troba cara la requadra amb en quadrat verd
def facedetect(foto):
    """
    Fucnión que recuadra la cara o caras de una iamagen
    :param foto: objeto imagen
    :return: none
    """
    faces = faceClassif.detectMultiScale(foto,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    for (x, y, w, h) in faces:
        marginX = int(x / 50)
        marginY = int(y / 50)
    try:
        cv2.rectangle(foto, (x - marginX, y - marginY), (x + w + marginX, y + h + marginY), (0, 255, 0), 1)
    except:
        print("No se han encontrado caras")


#   Deteccio de cara, si troba cara la tapa amb en quadrat negre
def facecover(foto):
    """
    Función que tapa de forma cuadrada la cara de un usuario
    :param foto: objeto imagen
    :return: devuelve la imagen con la cara tapada
    """
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
    """
    Función que crea una mascara circular si detecta una cara en la imagen
    :param image: obeto imagen
    :return: mascara aplicada a la imagen
    """
    faces = faceClassif.detectMultiScale(image,
                                         scaleFactor=1.1,
                                         minNeighbors=5,

                                         minSize=(30, 30),
                                         maxSize=(200, 200))

    for (x, y, w, h) in faces:
        marginX = int(x / 10)
        marginY = int(y / 10)
        #center_coordinates = x + w // 2, y + h // 2
        #radius = w // 2  # or can be h / 2 or can be anything based on your requirements
        # cv2.circle(foto, center_coordinates, radius, (0, 0, 100), 0)

    mask = np.zeros(image.shape, dtype=np.uint8)
    cv2.rectangle(mask,  (x + marginX, y + marginY), (x + w - marginX, y + h - marginY), (255, 255, 255), -1)

    # Bitwise-and for ROI
    ROI = cv2.bitwise_and(image, mask)

    # Crop mask and turn background white
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('mask', mask)
    x, y, w, h = cv2.boundingRect(mask)
    result = ROI[y:y + h, x:x + w]
    mask = mask[y:y + h, x:x + w]
    result[mask == 0] = (255, 255, 255)
    #Ara aqui vull fer una divisio de sa cara en 5 rectangles



    return result


def centresFoto(foto):
    """
    Función que devuelve las coordenadas del centro de la persona
    :param foto: objeto imagen
    :return: centroX, centroY
    """
    width, height, e = foto.shape
    faces = faceClassif.detectMultiScale(foto,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    for (x, y, w, h) in faces:
        centrey = int(y + (w / 2))
        centrex = int(x + (h / 2))
    try:
        return centrex, centrey
    except:
        print("No se han encontrado caras")

def cropDretaEsq(foto):
    """
      Función que devuelve dos imagenes cropeadas segun la cara
      :param foto: objeto imagen
      :return: dreta, esquerra
      """
    height, width, e = foto.shape
    faces = faceClassif.detectMultiScale(foto,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    for (x, y, w, h) in faces:
        centrey = int(y + (w / 2))
        centrex = int(x + (h / 2))
    try:
        dreta = foto[0:height, 0:centrex]
        esquerra = foto[0:height, centrex:width]
        return dreta, esquerra
    except:
        print("No s'ha trobat cara")



