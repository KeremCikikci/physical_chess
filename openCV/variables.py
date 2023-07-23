fx = 914.413655169
fy = 915.827825362
cx = 634.088633608
cy = 373.530293726
k1 = -0.474162217
k2 = 0.296860407
k3 = 0.000851414
k4 = -0.001612337

width = 1280
height = 720

color_threshold = .2

lowerBlue_hsv = (80, 60, 50)
upperBlue_hsv = (130, 185, 255)
lowerRed_hsv = (0, 10, 0) # (0, 100, 0)
upperRed_hsv = (60, 250, 255)

p1 = [100, 100] # sol alt
p2 = [120, 10] # sag üst
p3 = [50, 20]
p4 = [40, 30]

corners = [p1, p2, p3, p4]

squares = []

# Yukardan assaga harfler, soldan saga sayilar
contents = [["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"],
            ["Red", "Red", "Space", "Space", "Space", "Space", "Blue", "Blue"]]

horizontal = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

game_id = "wbg3MhJW"

moves = []
lastMove = ""