import math
import numpy as np

alphaRPM = 600
betaRPM = 600
gamaRPM = 66.67

alphaCycleStep = 600
betaCycleStep = 600
gamaCycleStep = 180

alphaRatio = 48/20

AlphaCircleStep = alphaCycleStep  * alphaRatio
BetaCircleStep = betaCycleStep
GamaCircleStep = gamaCycleStep

AlphaAngleSpeed = 60 / (alphaRPM/alphaRatio) / 360 # 600*200/(200*48/20)=250 RPM
BetaAnlgleSpeed = 60 / alphaRPM / 360 # 600 RPM
GamaAngleSpeed = 0.9 / 360 # 66.67 RPM

stepAlpha = 0
stepBeta = 0
stepGama = 90

stepperAngle = [stepAlpha, stepBeta, stepGama]

def calStep(deltaAngles):
    AlphaStep = deltaAngles[0] * AlphaCircleStep / 360
    BetaStep = deltaAngles[1] * BetaCircleStep / 360
    GamaStep = deltaAngles[2]

    return [AlphaStep, BetaStep, GamaStep]

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def calAngles(edge1, edge2, points):
    A, B, C = points
    B_, C_ = [0, edge1], [edge1, edge2]
    
    alpha = angle_between((0, edge1), B)
    beta = angle_between((0, edge2), (C[0]-B[0], C[1]-B[1]))
    gama = angle_between((0, -edge1), (B[0]-C[0], B[1]-C[1]))
    
    return [alpha, beta, gama]

def calTime(event):
    alphaTime = AlphaAngleSpeed * event[0]
    betaTime = BetaAnlgleSpeed * event[1]
    gamaTime = GamaAngleSpeed * event[2]

    return max(alphaTime, betaTime, gamaTime)

def calIntersectionPoints(circle1, circle2): #circle = (x, y, r)
    x0, y0, r0 = circle1
    x1, y1, r1 = circle2

    d = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None, None
    # One circle within other
    if d < abs(r0-r1):
        return None, None
    # coincident circles
    if d == 0 and r0 == r1:
        return None, None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3), (x4, y4)

Origin = [0, 0]
Point = [38, 24]
pipe1Size = 30
pipe2Size = 20

circle1 = (Origin[0], Origin[1], pipe1Size)
circle2 = (Point[0], Point[1], pipe2Size)
point1, point2 = calIntersectionPoints(circle1, circle2)

A, B, C = [0,0], point2, Point

if point1 != None:
    deltaAngles = [stepperAngle[0] - calAngles(pipe1Size, pipe2Size, [A, B, C])[0], stepperAngle[1] - calAngles(pipe1Size, pipe2Size, [A, B, C])[1], stepperAngle[2] - calAngles(pipe1Size, pipe2Size, [A, B, C])[2]]
    
    time = calTime(deltaAngles)

    print(time)
    #print(time, [A,B,C], angles)
