import cv2
from ultralytics import YOLO
import numpy as np

from datetime import timedelta, datetime
import serial
import copy
import time

import berserk
import chess
from PIL import ImageGrab

# from variables import *
# from initializer import *
# from functions import *
from f import *

SYMDETECTION = False

corners = []

def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_value = board[y, x]
        print(f"Pixel değeri ({x}, {y}): {pixel_value}")
        corners.append(pixel_value)

# Foto cekme
try:
    cap = cv2.VideoCapture(0)

    ret, board = cap.read()
    cv2.imwrite("board.jpg", board)
except:
    pass

# Fotodan satranc tahtasini secme
cv2.namedWindow("Fotoğraf")
cv2.setMouseCallback("Fotoğraf", on_mouse_click)

# icerigi kaydetme

# lichess i cekme senkron etme

# arduinodan mesaj okuma

# butona basildiginda foto cekme ve icerigi kaydetme

# önceki icerik ile karsilatirma 

# fark bulma

# hamle bulma

# hamleyi lichesste oynama

# lichesste foto cekme ve karsilastirip hamle bulma

# hamleyi print etme ve robota oynatma
