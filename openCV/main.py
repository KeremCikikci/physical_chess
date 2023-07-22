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

from variables import *
from initializer import *
from functions import *

session, client, chess_ = ini_chess()

ret, board = cap.read()

board, corners = findSym(board, corners)

squareWidth, squareHeight = getSize(corners)

color_threshold2 = .1

lowerWhite_hsv = (0, 0, 50)#(80, 60, 50)#cv2.cvtColor(np.uint8([[lowerOr]]), cv2.COLOR_BGR2HSV)
upperWhite_hsv = (5, 3, 255)#(130, 185, 255)
lowerBlack_hsv = (0, 0, 0)# (0, 10, 0)
upperBlack_hsv = (5, 3, 50)

x1, y1, x2, y2 = 394, 160, 905, 670

horizontal2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h']#['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

def getChanges2(preList, list):
    changes = []
    for i in range(len(preList)):
        for a in range(len(preList[0])):
            if preList[i][a] != list[i][a]:
                changes.append(horizontal2[i] + str(a + 1))
    
    return changes

def getMove2(changes):
    from_ = ""
    to_ = ""

    for change in changes:
        letter = horizontal2.index(change[0])
        number = int(change[-1]) - 1
        if contents[letter][number] == "Space":
            from_ = change
        else:
            to_ = change

    return from_ + to_

def findContents(x1, y1, x2, y2):
    ss = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    width, height = ss.size
    total_pixels = width * height / 64
    squareWidth, squareHeight = width // 8, height // 8
    ss.save("s.jpg")
    for h in range(0, 8):
        for n in range(0, 8):
            square = (h * squareWidth, n * squareHeight, (h+1)*squareWidth, (n+1)*squareHeight)
            cropped = np.array(ss.crop(square))
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

            mask_white = cv2.inRange(cropped, lowerWhite_hsv, upperWhite_hsv)
            mask_black = cv2.inRange(cropped, lowerBlack_hsv, upperBlack_hsv)

            white_pixels = np.sum(mask_white > 0)
            white_intensity = white_pixels / total_pixels

            black_pixels = np.sum(mask_black > 0)
            black_intensity = black_pixels / total_pixels
            c = "Space"

            if white_intensity > color_threshold2 or black_intensity > color_threshold2:
                if white_intensity >= black_intensity:
                    c = "Red"
                else:
                    c = "Blue"
          
            contents[7-h][n] = c

            cv2.imwrite("crop/"+horizontal2[h] + str(n+1) + ".jpg", cropped)

def cropSquares(contents, board):
    squares.clear()
    for h in range(0, 8): # width
        for n in range(0, 8): # height
            square = Square(horizontal[h] + str(n + 1))
            square.crop(board, corners[3][0] + h * squareWidth , corners[3][1] - n * squareHeight, squareWidth, squareHeight)

    for square in squares:
        content = square.getContent()
        name = square.name
        
        contents[horizontal.index(name[0])][int(name[-1])-1] = content
    return contents
    
#contents = cropSquares(contents, board)
findContents(x1, y1, x2, y2)
print(contents)
preContents = []

while True:
    current_time = datetime.now()
    getMove_time = datetime.now()
    
    read = arduino.readline()

    # Hamle cekme
    if getMove_time >= getMove_trigger:
        getMove_trigger = getMove_time + timedelta(seconds=.7)
        preContents = copy.deepcopy(contents)
        print("pre", preContents)
        findContents(x1, y1, x2, y2)
        changes = getChanges2(preContents, contents)
        print("con: ", contents)
        print("hamle cekme changes: ", changes)
        if len(changes) == 2:
            move = getMove2(changes)

            from_ = move[:2]
            to_ = move[-2:]

            letterF = horizontal.index(from_[0])
            numberF = int(from_[-1]) - 1
            letterT = horizontal.index(to_[0])
            numberT = int(to_[-1]) - 1

            contents[letterF][numberF] = "Space"
            contents[letterT][numberT] = "Red"
            preContents = copy.deepcopy(contents)
            changes=[]
            #chess_.push_uci(move)

    if str(read[0:4]) == "b'move'" and current_time >= next_trigger:
        next_trigger = current_time + timedelta(seconds=.9)
        changes=[]
        ret, board = cap.read()

        board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)

        preContents = copy.deepcopy(contents)
        contents = cropSquares(contents, board)
        print(preContents, contents)
        changes = getChanges(preContents, contents)
        print("changes: ", changes)
        if len(changes) == 2:
            move = getMove(changes)
            print("kendi hamlen: ", move)
            try:
                berserk.clients.Board(session=session).make_move(game_id, move)
                time.sleep(8)
            except:
                print('hata')


#     # if getMove_time >= getMove_trigger and chess_.turn == chess.WHITE:
#     #     moves_ = client.games.export(game_id)['moves']
#     #     moves = moves_.split()
#     #     getMove_trigger = getMove_time + timedelta(seconds=.7)
        
#     #     if len(moves) % 2 == 1:
#     #         lastMove = moves[-1]

#     #         # Rakip oynamasi
#     #         try:
#     #             moves_ = client.games.export(game_id)['moves']
#     #             moves = moves_.split()
#     #             uci_move = chess_.push_san(moves[-1]).uci()
#     #         except:
#     #             chess_.turn = chess.BLACK
#     #         print("rakip oynuyor: ", uci_move)

#     #         from_ = uci_move[:2]
#     #         to_ = uci_move[-2:]

#     #         letterF = horizontal.index(from_[0])
#     #         numberF = int(from_[-1]) - 1
#     #         letterT = horizontal.index(to_[0])
#     #         numberT = int(to_[-1]) - 1

#     #         contents[letterF][numberF] = "Space"
#     #         contents[letterT][numberT] = "Red"
            
#     #         print(contents)
        

#     # if str(read[0:4]) == "b'move'" and current_time >= next_trigger and chess_.turn == chess.BLACK:
#     #     next_trigger = current_time + timedelta(seconds=.9)
        
#     #     ret, board = cap.read()

#     #     board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)

#     #     preContents = copy.deepcopy(contents)

#     #     contents = cropSquares(contents)

#     #     # önceki hali ile karsilastir
#     #     changes = getChanges(preContents, contents)
#     #     print("changes: ", changes)
#     #     if len(changes) == 2:
#     #         # hamle kodunu olustur
#     #         move = getMove(changes)
#     #         print("kendi hamlen: ", move)
            
#     #         try:
#     #             berserk.clients.Board(session=session).make_move(game_id, move)
#     #             moves_ = client.games.export(game_id)['moves']
#     #             moves = moves_.split()
#     #             chess_.push_uci(move)
                
#     #             print(contents)
#     #         except:
#     #             print("yanlis hamle tespiti")

#     #             # önceki hali ile karsilastir
#     #             changes = getChanges(preContents, contents)
#     #             print("pre: ", preContents)
#     #             print("con: ", contents)
#     #             print("changes: ", changes)
                
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


cap.release()
cv2.destroyAllWindows()