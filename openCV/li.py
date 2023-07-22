import time
from PIL import ImageGrab
import cv2
import numpy as np
import copy

x1, y1, x2, y2 = 406, 163, 894, 652

horizontal2 = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

lowerWhite_hsv = (100, 220, 200)#(80, 60, 50)#cv2.cvtColor(np.uint8([[lowerOr]]), cv2.COLOR_BGR2HSV)
upperWhite_hsv = (255, 255, 255)#(130, 185, 255)
lowerBlack_hsv = (0, 0, 0)# (0, 10, 0)
upperBlack_hsv = (105, 155, 155)

color_threshold = .12

contents = [["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"]]

def getChanges(preList, list):
    changes = []
    for i in range(len(preList)):
        for a in range(len(preList[0])):
            if preList[i][a] != list[i][a]:
                changes.append(horizontal2[i] + str(a + 1))
    
    return changes

def getMove(changes):
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

            mask_white = cv2.inRange(cropped, lowerWhite_hsv, upperWhite_hsv)
            mask_black = cv2.inRange(cropped, lowerBlack_hsv, upperBlack_hsv)

            white_pixels = np.sum(mask_white > 0)
            white_intensity = white_pixels / total_pixels

            black_pixels = np.sum(mask_black > 0)
            black_intensity = black_pixels / total_pixels
            c = "Space"

            if white_intensity > color_threshold or black_intensity > color_threshold:
                if white_intensity >= black_intensity:
                    c = "White"
                else:
                    c = "Black"
            if h == 0 and n == 0:
                print(white_intensity, black_intensity)

                print(c)    
            contents[h][n] = c
            
            #cropped.save("crop/"+horizontal[h] + str(n+1) + ".jpg")
    


findContents(x1, y1, x2, y2)
preContents = copy.deepcopy(contents)
print(preContents)
# a = input("bas")
# findContents(x1, y1, x2, y2)
# print(contents)
# changes = getChanges(preContents, contents)
# x = getMove(changes)
# print(x)