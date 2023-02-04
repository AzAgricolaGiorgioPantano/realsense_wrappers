#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
# Import time
import time


try:
    # Serial numbers of cameras
    device_lst = ["846112072041", "845112070847"]

    print("reset_cameras:: Reset procedure started")
    time.sleep(1) 

    print("reset_cameras:: reset start")
    ctx = rs.context()
    devices = ctx.query_devices()
    for dev in devices:
        dev.hardware_reset()
    print("reset_cameras:: reset done")

finally:
    pass