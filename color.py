import cv2
import numpy as np

content = None
threshold = .1

lowerBlue_hsv = (100, 115, 70) # (100, 120, 50)
upperBlue_hsv = (130, 185, 255)
lowerRed_hsv = (150, 120, 60) # (0, 10, 0)
upperRed_hsv = (250, 195, 250)

# resmi ac
#source = "assets/2.jpg"
source = "assets/a.jpg"
board = cv2.imread(source)

mask_blue = cv2.inRange(board, lowerBlue_hsv, upperBlue_hsv)
mask_red = cv2.inRange(board, lowerRed_hsv, upperRed_hsv)

result = cv2.bitwise_and(board, board, mask=mask_red)
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