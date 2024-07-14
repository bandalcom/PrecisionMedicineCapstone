import pyrealsense2 as rs
import cv2
import numpy as np
import mediapipe as mp
import time
import math as m
import utils.calculation as Cal
import utils.camera as Cam
import utils.color as Col
import utils.guide as Guide

# MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Determine camera type and open the appropriate stream
use_realsense = Cam.is_realsense_camera()

if use_realsense:
    print("Using RealSense Camera")
    pipeline = Cam.open_realsense_camera()
else:
    print("Using Raspberry Pi Camera")
    cap = Cam.open_raspberry_pi_camera()

# Create a window to display the video
cv2.namedWindow('Camera View', cv2.WINDOW_AUTOSIZE)

# Initialize lists to store landmarks data
landmarks_data = [[] for _ in range(33)]

try:
    while True:
        if use_realsense:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
        else:
            ret, color_image = cap.read()
            if not ret:
                continue

        # To improve performance, optionally mark the image as not writeable to pass by reference
        color_image.flags.writeable = False
        color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
        results = pose.process(color_image)

        # Draw the pose annotation on the image.
        color_image.flags.writeable = True
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
        h, w, _ = color_image.shape

        """if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                color_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract landmark information and save to the respective lists
            for id, landmark in enumerate(results.pose_landmarks.landmark):
                cx, cy, cz = int(landmark.x * w), int(landmark.y * h), int(landmark.z * w)
                landmarks_data[id].append([cx, cy, cz])"""

        # Display the resulting image
        lm = results.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
        r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
        l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
        l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
        l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
        l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)
        Guide.NerdNeckSlice(color_image,l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y, l_ear_x, l_ear_y, l_hip_x, l_hip_y)
        cv2.imshow('Camera View', color_image)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    if use_realsense:
        pipeline.stop()
    else:
        cap.release()
    cv2.destroyAllWindows()

# Print the length of each list to verify the data
for i, landmark_list in enumerate(landmarks_data):
    print(f'Landmark {i} data length: {len(landmark_list)}')
