import serial
import time
from datetime import timedelta, datetime
import berserk

next_trigger = datetime.now()

API_TOKEN = 'lip_I07d8jqSPHAYzacfCumR'
session = berserk.TokenSession(API_TOKEN)
client = berserk.Client(session=session)

game_id = '0CUMIihK'

# FETCH MOVES
#print(client.games.export(game_id)['moves'])

# FETCH TIME
#print(client.games.export(game_id)["clocks"])


# MAKE MOVE
#berserk.clients.Board(session=session).make_move(game_id, 'c1f4')

moveTurn = 0

time_ = "87654321"

digits = ["00000011", "10011111", "00100101", "00001101", "10011001", "01001001", "01000001", "00011011", "00000001", "00001001"] # Common Anode

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=0.1)

def clock(time_):
    leds=[]
    if len(time_) != 8:
        print("time size does not fit in digits")
    else:
        for i in range(len(time_)):
            ### DIGIT ###
            digit = ""
            # pre 0s
            for pre0 in range(7-i):
                digit += '0'
            # 0
            digit += '1'
            
            # post 0s
            for post0 in range(8-len(digit)):
                digit += '0'
            
            ### NUMBER ###
            number = digit[::-1] + digits[int(time_[i])]
            
            ### binary string to decimal string conversation ###
            integer = 0
            for i in range(0, len(number)):
                if number[15-i] == "1":
                    integer += 2**i

            leds.append(str(integer))
        
        print("The message was succesfully sended")
    
    return leds

def sendMessage(type, messages):
    for m in range(1, len(messages) + 1):
        mType = type + str(m) + " "
        mType += messages[m-1]
        arduino.write(bytes(mType, 'utf-8'))
        time.sleep(.1)
        #arduino.write(bytes("\n", 'utf-8'))

def step(x, y, z):
    steps = "{} {} {}".format(x, y, z)
    return steps

def makeMove(move):
    berserk.clients.Board(session=session).make_move(game_id, move)

def getLastTimes(times):
    global moveTurn
    
    if len(times) % 2 == 0:
        player1 = times[-1]//100
        player2 = times[-2]//100
    else:
        player1 = times[-2]//100
        player2 = times[-1]//100

    moveTurn = (moveTurn + 1)%2

    return player1, player2

def outTime(players):
    out = ""
    for player in players:
        #player /= 100
        td_str = str(timedelta(seconds=player))
        x = td_str.split(':')
        out += (x[1] + x[2])

    print(out)
    return out

time.sleep(2)

sendMessage("C", clock(time_))

p1Time, p2Time = getLastTimes(client.games.export(game_id)["clocks"])

while True:
    current_time = datetime.now()

    read = arduino.readline()
    move = 'h2h4'

    # Bunu her saniye icin yap
    if current_time >= next_trigger:
        if moveTurn == 0:
            p1Time -= 1
        else:
            p2Time -= 1
        
        time_ = outTime([p1Time, p2Time])
        sendMessage("C", clock(time_))

        next_trigger = current_time + timedelta(seconds=.9)
    
    if str(read[0:4]) == "b'move'":
        makeMove(move)
        time.sleep(.4)
        p1Time, p2Time = getLastTimes(client.games.export(game_id)["clocks"])
        time_ = outTime([p1Time, p2Time])
        sendMessage("C", clock(time_))

