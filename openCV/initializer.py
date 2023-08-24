import cv2
from variables import squares, lowerBlue_hsv, upperBlue_hsv, lowerRed_hsv, upperRed_hsv, color_threshold
import numpy as np

import chess
import berserk

from datetime import timedelta, datetime
from ultralytics import YOLO
import serial


from variables import width, height

class Square:
    def __init__(self, name):
        self.name = name
        squares.append(self)
        self.square = None
        self.content = None

    def crop(self, board, x, y, w, h):
        square = board[y-h:y, x:x+w]

        self.square = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)
        
        cv2.imwrite("croppedImage/" + self.name + ".jpg", self.square)

    def getContent(self):
        square = self.square
        
        total_pixels = square.shape[0] * square.shape[1]

        mask_blue = cv2.inRange(square, lowerBlue_hsv, upperBlue_hsv)
        mask_red = cv2.inRange(square, lowerRed_hsv, upperRed_hsv)

        # Turuncu icin
        blue_pixels = np.sum(mask_blue > 0)
        blue_intensity = blue_pixels / total_pixels

        # Kirmizi icin
        red_pixels = np.sum(mask_red > 0)
        red_intensity = red_pixels / total_pixels
        
        if red_intensity > color_threshold or blue_intensity > color_threshold:
            if blue_intensity >= red_intensity:
                self.content = "Blue"
            else:
                self.content = "Red"
        else:
            self.content = "Space"

        return self.content
    
def ini_chess():
    API_TOKEN = 'lip_I07d8jqSPHAYzacfCumR'
    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    chess_ = chess.Board()

    return session, client, chess_

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

next_trigger = datetime.now()
getMove_trigger = datetime.now()
clock_trigger = datetime.now()

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0)

model = YOLO('weights/best.pt')

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)