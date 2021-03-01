import argparse
import glob
import os

import cv2

def punts(mat,yolo):

    width, height, inference_time, results = yolo.inference(mat)

    if not results:
        #   Aqui hauriem de cridar a l'altre metode
        return -1

    #   Si tenim una ma com a mínim, cream finestra i mostram

    for detection in results:
        id, name, confidence, x, y, w, h = detection
        cx = x + (w / 2)
        cy = y + (h / 2)
        label = str(cx)

        #print(x,y)
        # cv2.imwrite("export.jpg", mat)
        return (x,y,w,h)



