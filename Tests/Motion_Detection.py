import cv2
import numpy as np

faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


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


def checkMoviment(img1, img2):
    # open or read the images
    img1 = cv2.imread('Ma_abaix.jpg')
    img2 = cv2.imread('Ma_adalt.jpg')


    # resize the images to speed up processing
    img1 = cv2.resize(img1, (640, 480))
    img2 = cv2.resize(img2, (640, 480))

    # display resized images

    # Convert images to grayscale. This reduces matrices from 3 (R, G, B) to just 1
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # Cercam cares per taparles amb un quadrat
    faces = faceClassif.detectMultiScale(gray1,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    for (x, y, w, h) in faces:
        cv2.rectangle(gray1, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 0, 0), -1)
    faces = faceClassif.detectMultiScale(gray2,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         maxSize=(200, 200))
    for (x, y, w, h) in faces:
        cv2.rectangle(gray2, (x - 20, y - 20), (x + w + 20, y + h + 20), (0, 0, 0), -1)

    # Blur the images to get rid of sharp edges/outlines. This will improve the processing
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Test
    _, contours2, hierarchy2 = cv2.findContours(gray1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours2]
    max_index = np.argmax(areas)
    cnt = contours2[max_index]

    print(areas)
    x1, y1, w, h = cv2.boundingRect(cnt)
    x1 = int(x1 + w / 2)
    y1 = int(y1 + h / 2)
    print("Punts incials")
    print(x1, y1)

    '''
    # display blurred images
    
    # obtain the difference between the two images & display the result
    imgDelta = cv2.absdiff(gray1, gray2)
    
    
    # coonvert the difference into binary & display the result
    thresh = cv2.threshold(imgDelta, 25, 255, cv2.THRESH_BINARY)[1]
    
    
    # dilate the thresholded image to fill in holes & display the result
    thresh = cv2.dilate(thresh, None, iterations=2)
    '''

    # find contours or continuous white blobs in the image
    _, contours, hierarchy = cv2.findContours(gray2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt = contours[max_index]

    # draw a bounding box/rectangle around the largest contour
    x2, y2, w, h = cv2.boundingRect(cnt)
    x2 = int(x2 + w / 2)
    y2 = int(y2 + h / 2)
    print("Punts finals")
    print(x2, y2)
    # cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),2)

    # display the original image for reference
    cv2.imshow("Proces", np.hstack([gray1, gray2]))
    # Pintam text i linea
    img2 = cv2.putText(img2, 'Punt inicial', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    img2 = cv2.putText(img2, 'Punt final', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.line(img2, (x1, y1), (x2, y2), (255, 0, 0), 5)

    img1 = cv2.putText(img1, 'Punt inicial', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    img1 = cv2.putText(img1, 'Punt final', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.line(img1, (x1, y1), (x2, y2), (255, 0, 0), 5)

    cv2.imshow("Ma adalt i abaix", np.hstack([img1, img2]))
    # wait for key press and then terminate all open windows
    moviment(x1, y1, x2, y2)


def main():
    checkMoviment("Ma_abaix.jpg", "Ma_adalt.jpg")
    if cv2.waitKey(0) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        exit()


main()
