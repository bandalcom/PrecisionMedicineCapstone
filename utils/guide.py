# side view body allignment guide function
import cv2
from .calculation import *
from .color import *
def sideAlign(image,l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y):
    offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
    if offset < 100:
        # Case of two shoulder points are alligned properly
        # r_shldr point color varies by situation
        print('Aligned')
        cv2.circle(image, (l_shldr_x, l_shldr_y), 14, green, 1)
        cv2.circle(image, (r_shldr_x, r_shldr_y), 7, green, -1)
    else:
        print('Not Aligned')
        cv2.circle(image, (l_shldr_x, l_shldr_y), 14, black, 1)
        cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)

def NerdNeckSlice(image,l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y, l_ear_x, l_ear_y, l_hip_x, l_hip_y):
    standard = findStandard(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y, l_ear_x, l_ear_y)
    neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
    torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)
    if neck_inclination < 15:
        neck_state = 0
        cv2.circle(image, (l_shldr_x, l_shldr_y - standard), 14, green, 1)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, green, -1)
        print('Alive')
    else:
        neck_state = 1
        cv2.circle(image, (l_shldr_x, l_shldr_y - standard), 14, black, 1)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, pink, -1)
        print('Dead')

    if torso_inclination < 10:
        torso_state=0
        cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 10)
        cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 10)
    else:
        torso_state=1
        cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), black, 10)
        cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), pink, 10)


    """if neck_state == 0 and torso_state==0:
        bad_frames = 0
        good_frames += 1
    else:
        good_frames = 0
        bad_frames += 1"""