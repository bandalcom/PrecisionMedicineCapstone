import math as m
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2-x1)**2+(y2-y1)**2)
    return dist
def findStandard(x1, y1, x2, y2, x3, y3):
    #어깨 중앙 포인트 ~ 관자도리 포인트까지의 거리
    center_shldr_x = (x2+x1)/2
    center_shldr_y = (y2+y1)/2
    standard = findDistance(x3, y3, center_shldr_x, center_shldr_y)
    return int(standard)
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 -y1)*(-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
    degree = int(180/m.pi)*theta
    return degree
def sendWarning(x):
    pass