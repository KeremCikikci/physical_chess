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
from colorama import init, Fore, Style

init(autoreset=True)

SYMDETECTION = False
SELECTBOARD = False

gameID = 'D8wSAfSk'

contents = [["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"],
            ["BLACK", "BLACK", "SPACE", "SPACE", "SPACE", "SPACE", "WHITE", "WHITE"]]

liContents = copy.deepcopy(contents)

alphabeth = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

color_threshold = .2
color_threshold_lichess = .1

lowerBlue_hsv = (100, 120, 50)
upperBlue_hsv = (130, 185, 255)
lowerRed_hsv = (0, 100, 0) # (0, 10, 0)
upperRed_hsv = (60, 250, 255)

lowerWhite_hsv = (0, 0, 50)#(80, 60, 50)#cv2.cvtColor(np.uint8([[lowerOr]]), cv2.COLOR_BGR2HSV)
upperWhite_hsv = (5, 3, 255)#(130, 185, 255)
lowerBlack_hsv = (0, 0, 0)# (0, 10, 0)
upperBlack_hsv = (5, 3, 50)

x1, y1, x2, y2 = 400, 160, 905, 670

fx = 914.413655169
fy = 915.827825362
cx = 634.088633608
cy = 373.530293726
k1 = -0.474162217
k2 = 0.296860407
k3 = 0.000851414
k4 = -0.001612337

API_TOKEN = 'lip_I07d8jqSPHAYzacfCumR'
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0)

button_trigger = datetime.now()
getMove_trigger = datetime.now()
clock_trigger = datetime.now()

turn = "BLACK"

def fisheye_correction(img, fx, fy, cx, cy, k1, k2, k3, k4):
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float64)

    D = np.array([k1, k2, k3, k4], dtype=np.float64)

    corrected_img = cv2.fisheye.undistortImage(img, K, D, Knew=K)
    return corrected_img

def getContent(board, EXAMPLE = False):
    for x in range(8):
        for y in range(8):
            square = board[topLeftCorner[1] + squareHEIGHT * y:topLeftCorner[1] + squareHEIGHT * (y+1), topLeftCorner[0] + squareWIDTH * x:topLeftCorner[0] + squareWIDTH * (x+1)]
            square = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)

            if EXAMPLE:
                cv2.imwrite('assets/' + alphabeth[x] + str(8-y) + ".jpg", square)

            mask_black = cv2.inRange(square, lowerBlue_hsv, upperBlue_hsv)
            mask_white = cv2.inRange(square, lowerRed_hsv, upperRed_hsv)

            # Mavi icin
            black_pixels = np.sum(mask_black > 0)
            black_intensity = black_pixels / square_pixels

            # Kirmizi icin
            white_pixels = np.sum(mask_white > 0)
            white_intensity = white_pixels / square_pixels
            
            content = "SPACE"

            if white_intensity > color_threshold or black_intensity > color_threshold:
                if black_intensity >= white_intensity:
                    content = "BLACK"
                else:
                    content = "WHITE"

            contents[x][7 - y] = content

    return contents

def getLiContent():
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
            c = "SPACE"

            if white_intensity > color_threshold_lichess or black_intensity > color_threshold_lichess:
                if white_intensity >= black_intensity:
                    c = "WHITE"
                else:
                    c = "BLACK"
            
            liContents[7-h][n] = c
    
    return liContents

def getChanges(list1, list2):
    changes = []
    for i in range(len(list1)):
        for a in range(len(list1[0])):
            if list1[i][a] != list2[i][a]:
                changes.append(alphabeth[i] + str(a + 1))
    
    return changes

def getMove(changes, preContents, turn):
    captured = None
    
    letter = alphabeth.index(changes[0][0])
    number = int(changes[0][1]) - 1

    # Rok durumu
    if len(changes) == 4:
        if all(element in changes for element in ['e1', 'f1', 'g1', 'h1']) or all(element in changes for element in ['e8', 'f8', 'g8', 'h8']):
            return "KISA"
        else:
            return "UZUN"
    if len(changes) == 2:
        if contents[letter][number] != "SPACE":
            change = preContents[alphabeth.index(changes[1][0])][int(changes[1][1]) - 1]
            print(change)
            if change != "SPACE" and change == turn:
                captured = changes[1]

            return changes[1] + changes[0], captured
        else:
            change = preContents[alphabeth.index(changes[0][0])][int(changes[0][1]) - 1]
            print(change)
            if change != "SPACE" and change == turn:
                captured = changes[0]

            return changes[0] + changes[1], captured

def button(turn = "BLACK"):
    preContents = copy.deepcopy(contents)
    ret, board = cap.read()
    try:
        board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)
    except:
        ret, board = cap.read()
        board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)

    _contents = getContent(board)

    # önceki icerik ile karsilatirma 
    changes = getChanges(preContents, _contents)
    print(changes)
    if len(changes) == 2 or len(changes) == 4:
        # hamle bulma
        move, captured = getMove(changes, preContents, turn)
        if move == "KISA":
            move = "e8g8"
        elif move == "UZUN":
            move = "e8c8"

        print(f"{Fore.BLUE}{move}{Style.RESET_ALL}")
        try:
            #hamleyi lichesste oynama
            berserk.clients.Board(session=session).make_move(gameID, move)
            turn = "WHITE"
        except:
            try:
                move = move[2] + move[3] + move[0] + move[1] 

                berserk.clients.Board(session=session).make_move(gameID, move)
                turn = "WHITE"
            except Exception as e:
                print(f"{Fore.GREEN}{e}{Style.RESET_ALL}")
                turn = "BLACK"

if SELECTBOARD:
    corners = []
else:
    corners = None
    try:
        with open("info.txt", 'r') as file:
            file.seek(0)
            _ = file.readline()
            _list = _.split()
            _list = list(map(int, _list))

            corners = [[_list[i], _list[i+1]] for i in range(0, len(_list), 2)]

    except Exception as e:
        print(f'Error: {e}')

def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel_loc = [x, y]
        corners.append(pixel_loc)

# Foto cekme
try:
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    ret, board = cap.read()
    board = fisheye_correction(board, fx, fy, cx, cy, k1, k2, k3, k4)
    cv2.imwrite("board.jpg", board)
except:
    cap = cv2.VideoCapture(0)

    ret, board = cap.read()
    cv2.imwrite("board.jpg", board)

# Fotodan satranc tahtasini secme
if SELECTBOARD:
    cv2.namedWindow("Select Corners")
    cv2.setMouseCallback("Select Corners", on_mouse_click)

    while True:
        cv2.imshow("Select Corners", board)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if len(corners) >= 4:
            break

    cv2.destroyAllWindows()
    cap.release()

    try:
        with open("info.txt", 'w+') as file:
            _corners = [loc for line in corners for loc in line]
            _ = " ".join(map(str, _corners))
            file.write(_)

    except Exception as e:
        print(f'Error: {e}')

topLeftCorner = corners[0]

# Kare boyutunu bulma
squareWIDTH = (corners[1][0] - topLeftCorner[0]) // 8
squareHEIGHT = (corners[3][1] - corners[0][1]) // 8

square_pixels = squareWIDTH * squareHEIGHT

# icerigi kaydetme
contents = getContent(board, EXAMPLE=True)

# lichess i cekme senkron etme
liContents = getLiContent()

if liContents == contents:
    print_ = "Oyun Tahtasi senkron ✔"
    print(f"{Fore.GREEN}{print_}{Style.RESET_ALL}")
else:
    print_ = "Oyun Tahtasi senkron Degil ✗"
    print(f"{Fore.RED}{print_}{Style.RESET_ALL}")

    differences = []
    for i in range(len(contents)):
        for j in range(len(contents[i])):
            if contents[i][j] != liContents[i][j]:
                differences.append([i, j])

    for i, j in differences:
        _1 = contents[i][j]
        _2 = liContents[i][j]
        format_1 = f"{Fore.RED}{_1}{Style.RESET_ALL}"
        format_2 = f"{Fore.RED}{_2}{Style.RESET_ALL}"
        print(f"({i}, {j}): {format_1} (Oyun Tahtasi) -> {format_2} (Lichess)")

# arduinodan mesaj okuma
while True:
    button_time = datetime.now()

    if turn == "BLACK":
        a = input()
        try:
            read = arduino.readline().decode().strip()
        except:
            pass
        # butona basildiginda foto cekme ve icerigi kaydetme
        if (read == 'move' and button_time > button_trigger) or a == "a":
            button_trigger = button_time + timedelta(seconds=.7)

            button()
            turn = "WHITE"    
        else:
            print("cok fazla degisiklik")
            button()
    
    # lichesste foto cekme ve karsilastirip hamle bulma
    if turn == "WHITE":
        time.sleep(5)
        liContents = getLiContent()

        changes = getChanges(contents, liContents)

        if len(changes) == 2 or len(changes) == 4:
            # hamle bulma
            move, captured = getMove(changes, contents, turn)
            print(f"{Fore.CYAN}{move}{Style.RESET_ALL}")
            if captured != None:
                print(f"{Fore.YELLOW}{captured}{Style.RESET_ALL}")

            contents = copy.deepcopy(liContents)
            turn = "BLACK"

# hamleyi print etme ve robota oynatma
