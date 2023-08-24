import serial
import time
import math

ARDUINO = True

y = None # [mm]

a = 232 # birinci borunun uzunlugu [mm]
b = 223.5 # ikinci borunun uzunlugu [mm]
thirdArm = 125

squareWidth = 40 # [mm]

tahtaDistance = None# [mm]
originToBoard = 144#134 # [mm]
fayans = 10.8
circleOrigin = 97.3

#aAngles_ = [[102, 91], [90, 80], [80, 75], [73, 67], [67, 60], [60, 55], [52.5, 46], [44, 39]]
#bAngles_ = [[25, 25], [41, 42], [53, 53], [67, 67], [77, 77], [89, 91], [101, 101], [114, 116]]

aAngles_ = [[110, 84], [100, 76], [90, 71.5], [80, 64.5], [75, 57], [65, 52], [57, 45], [52, 37.5]]
bAngles_ = [[35, 30], [53, 45], [63, 57], [75, 68], [87, 80.5], [97, 92], [111, 104.2], [115, 114]]

rightPadding = 34

move = "g3h7" 

if ARDUINO:
    arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1)

    time.sleep(2)

alphabet = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

def karsi_aci_bul(c):
    # Cosinüs teoremi kullanarak açıyı hesapla
    numerator = a**2 + b**2 - c**2
    denominator = 2 * a * b
    cos_theta = numerator / denominator

    # Açıyı radyan cinsinden hesapla
    theta_radians = math.acos(cos_theta)

    # Radyanı dereceye çevir ve döndür
    theta_degrees = math.degrees(theta_radians)
    return theta_degrees

def karsi_aci_bul2(hyp, karsi):
    yan2 = hyp
    
    # Cosinüs teoremi kullanarak açıyı hesapla
    numerator = a**2 + yan2**2 - karsi**2
    denominator = 2 * a * yan2
    cos_theta = numerator / denominator

    # Açıyı radyan cinsinden hesapla
    theta_radians = math.acos(cos_theta)

    # Radyanı dereceye çevir ve döndür
    theta_degrees = math.degrees(theta_radians)
    return theta_degrees


xPoss = [None, None]
aAngles = [None, None, None, None]
bAngles = [None, None, None, None]
squareSize = 40
"""
# ilk kare yukarda
move = "a1"
x = alphabet[::-1].index(move[0]) * squareSize + squareSize / 2
y = (int(move[1])-1)
xPoss[0] = x + rightPadding
aAngles[0] = aAngles_[y][0]
bAngles[0] = bAngles_[y][0]

# ilk kare assada
x = alphabet[::-1].index(move[0]) * squareSize + squareSize / 2
y = (int(move[1])-1)
aAngles[1] = aAngles_[y][1]
bAngles[1] = bAngles_[y][1]

while True:
    message = "C " + str(xPoss[0]) + "_" + str(aAngles[0]) + "-" + str(aAngles[1]) + "+" + str(bAngles[0]) + "*" + str(bAngles[1]) 
    arduino.write(bytes(message, 'utf-8'))
    back = arduino.readline().decode().strip()
    if back == "C":
        back = arduino.readline().decode().strip()
        try:
            if float(back) == xPoss[0]:
                back = arduino.readline().decode().strip()
                try:
                    if float(back) == aAngles[0]:
                        back = arduino.readline().decode().strip()
                        try:
                            if float(back) == aAngles[1]:
                                back = arduino.readline().decode().strip()
                                try:
                                    if float(back) == bAngles[0]:
                                        back = arduino.readline().decode().strip()
                                        try:
                                            if float(back) == bAngles[1]:
                                                print("mesaj basari ile gönderildi")
                                                break
                                        except:
                                            pass
                                except:
                                    pass
                        except:
                            pass        
                        
                        print("mesaj basari ile gönderildi")
                        break
                except:
                    pass
        except:
            pass

while True:
    arduino.write(bytes("G", 'utf-8'))
    back = arduino.readline().decode().strip()

    if back == "G":
        while True:
            back = arduino.readline().decode().strip()
            print("G")
            if back == "O":
                break
        break

while True:
    arduino.write(bytes("T", 'utf-8'))
    back = arduino.readline().decode().strip()

    if back == "T":
        print("T")
        while True:
            back = arduino.readline().decode().strip()
            if back == "O":
                break
        break

while True:
    arduino.write(bytes("M", 'utf-8'))
    back = arduino.readline().decode().strip()

    if back == "M":
        print("M")
        while True:
            back = arduino.readline().decode().strip()
            if back == "O":
                break
        break
"""

# ilk kare yukarda
x = alphabet.index(move[0]) * squareWidth + squareWidth / 2
y = (int(move[1])-1)
xPoss[0] = x + rightPadding
aAngles[0] = aAngles_[y][0]
bAngles[0] = bAngles_[y][0]

# ilk kare assada
x = alphabet.index(move[0]) * squareWidth + squareWidth / 2
y = (int(move[1])-1)
aAngles[1] = aAngles_[y][1]
bAngles[1] = bAngles_[y][1]

# ikinci kare yukarda
x = alphabet.index(move[2]) * squareWidth + squareWidth / 2
y = (int(move[3])-1)
xPoss[1] = x + rightPadding
aAngles[2] = aAngles_[y][0]
bAngles[2] = bAngles_[y][0]

# ikinci kare assada
x = alphabet.index(move[2]) * squareWidth + squareWidth / 2
y = (int(move[3])-1)
aAngles[3] = aAngles_[y][1]
bAngles[3] = bAngles_[y][1]

# ilk kare yukarda
# x = alphabet.index(move[0]) * squareWidth + squareWidth / 2
# y = (int(move[1])-1) * squareWidth + squareWidth / 2

# tahtaDistance = yukarda

# h = tahtaDistance + thirdArm - circleOrigin + tahtaDistance + fayans

# y_ = y + originToBoard
# hyp = math.sqrt(h**2+y_**2)
# beta = round(karsi_aci_bul(hyp), 2)
# yükseklikAcisi = math.degrees(h/hyp)
# alpha =  round(karsi_aci_bul2(hyp, b) + yükseklikAcisi, 2)

# xPoss[0] = x
# aAngles[0] = alpha
# bAngles[0] = beta

# # ilk kare assada
# tahtaDistance = assada

# h = fayans + tahtaDistance + thirdArm - circleOrigin

# y_ = y + originToBoard
# hyp = math.sqrt(h**2+y_**2)
# beta = round(karsi_aci_bul(hyp), 2)
# yükseklikAcisi = math.degrees(h/hyp)
# alpha =  round(karsi_aci_bul2(hyp, b) + yükseklikAcisi, 2)

# aAngles[1] = alpha
# bAngles[1] = beta

# # ikinci kare yukarda
# x = alphabet.index(move[2]) * squareWidth + squareWidth / 2
# y = (int(move[3])-1) * squareWidth + squareWidth / 2

# tahtaDistance = yukarda

# h = fayans + tahtaDistance + thirdArm - circleOrigin

# y_ = y + originToBoard
# hyp = math.sqrt(h**2+y_**2)
# beta = round(karsi_aci_bul(hyp), 2)
# yükseklikAcisi = math.degrees(h/hyp)
# alpha =  round(karsi_aci_bul2(hyp, b) + yükseklikAcisi, 2)

# xPoss[1] = x
# aAngles[2] = alpha
# bAngles[2] = beta

# # ikinci kare assada
# tahtaDistance = assada

# h = fayans + tahtaDistance + thirdArm - circleOrigin

# y_ = y + originToBoard
# hyp = math.sqrt(h**2+y_**2)
# beta = round(karsi_aci_bul(hyp), 2)
# yükseklikAcisi = math.degrees(h/hyp)
# alpha =  round(karsi_aci_bul2(hyp, b) + yükseklikAcisi, 2)

# aAngles[3] = alpha
# bAngles[3] = beta

if ARDUINO:
    while True:
        message = "X " + str(xPoss[0]) + "_" + str(xPoss[1])
        print("1")

        arduino.write(bytes(message, 'utf-8'))
        
        back = arduino.readline().decode('utf-8', errors='ignore').strip()
        if back == "X":
            back = arduino.readline().decode().strip()
            try:
                if float(back) == xPoss[0]:
                    back = arduino.readline().decode().strip()
                    try:
                        if float(back) == xPoss[1]:
                            print("mesaj basari ile gönderildi")
                            break
                    except:
                        pass
            except:
                pass

    while True:
        message = "A " + str(aAngles[0]) + "_" + str(aAngles[1]) + "-" + str(aAngles[2]) + "+" + str(aAngles[3])
        arduino.write(bytes(message, 'utf-8'))
        back = arduino.readline().decode().strip()
        if back == "A":
            back = arduino.readline().decode().strip()
            try:
                if float(back) == aAngles[0]:
                    back = arduino.readline().decode().strip()
                    try:
                        if float(back) == aAngles[1]:
                            back = arduino.readline().decode().strip()
                            try:
                                if float(back) == aAngles[2]:
                                    back = arduino.readline().decode().strip()
                                    try:
                                        if float(back) == aAngles[3]:
                                            print("mesaj basari ile gönderildi")
                                            break
                                    except:
                                        pass
                            except:
                                pass                   
                    except:
                        pass
            except:
                pass

    while True:
        message = "B " + str(bAngles[0]) + "_" + str(bAngles[1]) + "-" + str(bAngles[2]) + "+" + str(bAngles[3])
        arduino.write(bytes(message, 'utf-8'))
        back = arduino.readline().decode().strip()
        if back == "B":
            back = arduino.readline().decode().strip()
            try:
                if float(back) == bAngles[0]:
                    back = arduino.readline().decode().strip()
                    try:
                        if float(back) == bAngles[1]:
                            back = arduino.readline().decode().strip()
                            try:
                                if float(back) == bAngles[2]:
                                    back = arduino.readline().decode().strip()
                                    try:
                                        if float(back) == bAngles[3]:
                                            print("mesaj basari ile gönderildi")
                                            break
                                    except:
                                        pass
                            except:
                                pass
                    except:
                        pass
            except:
                pass
    
    while True:
        arduino.write(bytes("G", 'utf-8'))
        back = arduino.readline().decode().strip()

        if back == "G":
            while True:
                back = arduino.readline().decode().strip()
                print("G")
                if back == "O":
                    break
            break
    
    while True:
        arduino.write(bytes("T", 'utf-8'))
        back = arduino.readline().decode().strip()

        if back == "T":
            print("T")
            while True:
                back = arduino.readline().decode().strip()
                if back == "O":
                    break
            break
        
    while True:
        arduino.write(bytes("S", 'utf-8'))
        back = arduino.readline().decode().strip()

        if back == "S":
            print("S")
            while True:
                back = arduino.readline().decode().strip()
                if back == "O":
                    break
            break
    
    while True:
        arduino.write(bytes("D", 'utf-8'))
        back = arduino.readline().decode().strip()

        if back == "D":
            print("D")
            while True:
                back = arduino.readline().decode().strip()
                if back == "O":
                    break
            break
            
print("olay basladi")            
print(move, xPoss, aAngles, bAngles)
