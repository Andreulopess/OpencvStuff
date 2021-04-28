from __future__ import print_function
from __future__ import division
import cv2
import imutils
import BGsub as bg
import ColorPellDominant as cp
import pandas as pd
import numpy as np


def filtreManual(maAdalt,maAbaix):

    maxRange, minRange = cp.agafarNas(maAbaix)

    print("Primer ma abaix")
    print(maxRange,minRange)
    bg.BGSubSimple(maAbaix,minRange,maxRange)

    print("Despres ma adalt")

    maxRange, minRange = cp.agafarNas(maAdalt)
    print(maxRange,minRange)
    bg.BGSubSimple(maAdalt,minRange,maxRange)


#Execucció
maAdalt = cv2.imread('Imatges/t1.png')
maAbaix = cv2.imread('Imatges/t2.png')
filtreManual(maAdalt,maAbaix)

if cv2.waitKey(0) & 0xFF == ord("q"):
    cv2.destroyAllWindows()
    exit()

