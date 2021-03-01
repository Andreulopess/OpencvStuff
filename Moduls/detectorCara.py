import cv2

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
    for (x, y, w, h) in faces:
        cv2.rectangle(foto, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 0, 0), -1)
