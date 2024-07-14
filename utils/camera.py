import pyrealsense2 as rs
import cv2
import numpy as np
import mediapipe as mp

def is_realsense_camera():
    ctx = rs.context()
    if len(ctx.devices) > 0:
        return True
    return False

def open_realsense_camera():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)
    return pipeline

def open_raspberry_pi_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise ValueError("Unable to open the Raspberry Pi camera")
    return cap