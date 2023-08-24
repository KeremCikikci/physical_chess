import numpy as np
import cv2

from variables import *
from initializer import model, cap

from serial import *
import berserk
import time

def getClosest(x, y, z):
    if abs(x-z) < abs(y-z):
        return x
    else:
        return y
    
def fisheye_correction(img, fx, fy, cx, cy, k1, k2, k3, k4):
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float64)

    D = np.array([k1, k2, k3, k4], dtype=np.float64)

    corrected_img = cv2.fisheye.undistortImage(img, K, D, Knew=K)
    return corrected_img

def sort_points(points):
    # X koordinatlarına göre sırala
    sorted_points = sorted(points, key=lambda x: x[0])

    # Sol üst ve sağ üst noktaları belirle
    leftmost = sorted_points[:2]
    rightmost = sorted_points[2:]

    # Sol üst ve sol alt noktaları belirle
    leftmost = sorted(leftmost, key=lambda x: x[1])
    (tl, bl) = leftmost

    # Sağ üst ve sağ alt noktaları belirle
    rightmost = sorted(rightmost, key=lambda x: x[1])
    (tr, br) = rightmost

    return [tl, tr, br, bl]

def getChanges(preList, list):
    changes = []
    for i in range(len(preList)):
        for a in range(len(preList[0])):
            if preList[i][a] != list[i][a]:
                changes.append(horizontal[i] + str(a + 1))
    
    return changes

def getMove(changes):
    from_ = ""
    to_ = ""

    for change in changes:
        letter = horizontal.index(change[0])
        number = int(change[-1]) - 1
        if contents[letter][number] == "Space":
            from_ = change
        else:
            to_ = change

    return from_ + to_

def findSym(board, corners):
    board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)

    prediction = model.predict(board)

    boxes = prediction[0].boxes

    if len(boxes) == 4:
        x1, y1, w1, h1 = boxes[0].xyxy[0]
        x2, y2, w2, h2 = boxes[1].xyxy[0]
        x3, y3, w3, h3 = boxes[2].xyxy[0]
        x4, y4, w4, h4 = boxes[3].xyxy[0]

        p1 = [int(getClosest(x1, w1, width / 2)), int(getClosest(y1, h1, height / 2))]
        p2 = [int(getClosest(x2, w2, width / 2)), int(getClosest(y2, h2, height / 2))]
        p3 = [int(getClosest(x3, w3, width / 2)), int(getClosest(y3, h3, height / 2))]
        p4 = [int(getClosest(x4, w4, width / 2)), int(getClosest(y4, h4, height / 2))]

        corners = [p1, p2, p3, p4]

        corners = sort_points(corners)

    else:
        print("eksik ve ya fazla sembol tespiti")
        findSym(board, corners)

    return board, corners

def getSize(corners):
    pts = np.array(corners, np.int32)
    pts = pts.reshape((-1, 1, 2))

    #cv2.polylines(board, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

    boardWidth, boardHeigt = abs(corners[1][0] - corners[0][0]), abs(corners[3][1] - corners[1][1])
    squareWidth, squareHeight = boardWidth // 8, boardHeigt // 8

    return squareWidth, squareHeight
