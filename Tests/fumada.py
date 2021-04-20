from __future__ import print_function
from __future__ import division
import cv2
import imutils
import BGsub as bg
import ColorPellDominant as cp
import pandas as pd
import numpy as np


maAdalt = cv2.imread('Imatges/Maadalt.jpg')
maAbaix = cv2.imread('Imatges/Mabaix.jpg')

cp.agafarNas(maAdalt)
nas = cv2.imread('fotosTest/_50.jpg')
nas = imutils.resize(nas,width=400)
mitja = np.mean(nas, axis=tuple(range(nas.ndim-1)))
std = np.std(nas, axis=tuple(range(nas.ndim-1)))
maxRange = mitja+2*std
minRange = mitja-2*std;
bg.BGSub2(maAdalt,maAbaix,minRange,maxRange)


cv2.waitKey(0)

