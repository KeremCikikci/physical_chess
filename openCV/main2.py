import cv2
from ultralytics import YOLO
import numpy as np

from datetime import timedelta, datetime
import serial
import copy
import time

import berserk
import chess

from variables import *
from initializer import *
from functions import *

session, client, chess_ = ini_chess()

ret, board = cap.read()

board, corners = findSym(board, corners)

squareWidth, squareHeight = getSize(corners)

def cropSquares(contents):
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
    
contents = cropSquares(contents)

print("baslangic: ", contents)

while True:
    current_time = datetime.now()
    getMove_time = datetime.now()
    
    read = arduino.readline()

    # Hamle cekme
    if getMove_time >= getMove_trigger and chess_.turn == chess.WHITE:
        moves_ = client.games.export(game_id)['moves']
        moves = moves_.split()
        getMove_trigger = getMove_time + timedelta(seconds=.7)
        
        if len(moves) % 2 == 1:
            lastMove = moves[-1]

            # Rakip oynamasi
            try:
                moves_ = client.games.export(game_id)['moves']
                moves = moves_.split()
                uci_move = chess_.push_san(moves[-1]).uci()
            except:
                chess_.turn = chess.BLACK
            print("rakip oynuyor: ", uci_move)

            from_ = uci_move[:2]
            to_ = uci_move[-2:]

            letterF = horizontal.index(from_[0])
            numberF = int(from_[-1]) - 1
            letterT = horizontal.index(to_[0])
            numberT = int(to_[-1]) - 1

            contents[letterF][numberF] = "Space"
            contents[letterT][numberT] = "Red"
            
            print(contents)
        

    if str(read[0:4]) == "b'move'" and current_time >= next_trigger and chess_.turn == chess.BLACK:
        next_trigger = current_time + timedelta(seconds=.9)
        
        ret, board = cap.read()

        board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)

        preContents = copy.deepcopy(contents)

        contents = cropSquares(contents)

        # önceki hali ile karsilastir
        changes = getChanges(preContents, contents)
        print("changes: ", changes)
        if len(changes) == 2:
            # hamle kodunu olustur
            move = getMove(changes)
            print("kendi hamlen: ", move)
            
            try:
                berserk.clients.Board(session=session).make_move(game_id, move)
                moves_ = client.games.export(game_id)['moves']
                moves = moves_.split()
                chess_.push_uci(move)
                
                print(contents)
                time.sleep(1)
            except:
                print("yanlis hamle tespiti")

                # önceki hali ile karsilastir
                changes = getChanges(preContents, contents)
                print("pre: ", preContents)
                print("con: ", contents)
                print("changes: ", changes)
                
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()