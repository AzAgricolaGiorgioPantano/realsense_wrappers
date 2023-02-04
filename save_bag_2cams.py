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

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] == ".bag":
    print("The given file is not of correct file format.")
    print("Only names of files are accepted, no extensions (i.e, .bag)")
    exit()
    

try:
    # Serial numbers of cameras
    device_lst = ["846112072041", "845112070847"]

    print("save_bags_2cams:: Saving procedure started")
    time.sleep(1) 

    for dev_nr in range(0,len(device_lst)):

        # Create pipeline
        pipeline = rs.pipeline()

        # Create a config object
        config = rs.config()

        # Set serial of the device
        config.enable_device(device_lst[dev_nr])

        # Enable frames
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

        # Path to bag file
        path = args.input + "_" + device_lst[dev_nr] + ".bag"

        # Tell config that we will use record a file of a path
        config.enable_record_to_file(path)

        profile = pipeline.start(config)
        device = profile.get_device()
        recorder = device.as_recorder()
        rs.recorder.pause(recorder)

        print("save_bags_2cams:: Start " + device_lst[dev_nr] + " recording: " + str(args.input))
        time.sleep(5) 
        rs.recorder.resume(recorder)
        i=0

        while i<10:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            i+=1
        
        rs.recorder.pause(recorder)

        print("save_bags_2cams:: Stop " + device_lst[dev_nr] + " recording: " + str(args.input))

        pipeline.stop()

finally:
    pass