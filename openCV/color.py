import cv2
import numpy as np

content = None
threshold = .1

lowerBlue_hsv = (0, 0, 50)#(80, 60, 50)#cv2.cvtColor(np.uint8([[lowerOr]]), cv2.COLOR_BGR2HSV)
upperBlue_hsv = (5, 3, 255)#(130, 185, 255)
lowerRed_hsv = (0, 0, 0)# (0, 10, 0)
upperRed_hsv = (5, 3, 50)#(60, 250, 255)

# resmi ac
#source = "assets/2.jpg"
source = "../assets/a7.jpg"
board = cv2.imread(source)

mask_blue = cv2.inRange(board, lowerBlue_hsv, upperBlue_hsv)
mask_red = cv2.inRange(board, lowerRed_hsv, upperRed_hsv)

result = cv2.bitwise_and(board, board, mask=mask_blue)
cv2.imshow("asda", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

total_pixels = board.shape[0] * board.shape[1]

# Mavi icin
blue_pixels = np.sum(mask_blue > 0)
blue_intensity = blue_pixels / total_pixels

# Kirmizi icin
red_pixels = np.sum(mask_red > 0)
red_intensity = red_pixels / total_pixels

# if or_intensity > or_threshold:
#     content = "Orange"


print(red_intensity, blue_intensity)