#####################################################
##               Read bag from file                ##
#####################################################

# First import library
from ctypes.wintypes import POINT
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

point = (400,300)

def click(event, x, y, flags, param):
  global point, pressed
  if event == cv2.EVENT_LBUTTONDOWN:
    print("Pressed",x,y)
    point = (x,y)

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
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    pipeline = rs.pipeline()
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

    # Configure the pipeline to stream the depth stream
    # Change this parameters according to the recorded bag file resolution
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

    # Start streaming from file
    pipeline.start(config)

    # align RGB to depth accordint to: https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/align-depth2color.py
    align_to = rs.stream.depth
    align = rs.align(align_to)

    # Create opencv window to render image in
    #cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Color frame", cv2.WINDOW_AUTOSIZE)

    cv2.setMouseCallback("Color frame",click)

    # Create colorizer object
    colorizer = rs.colorizer()


    # Streaming loop
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        aligned_frames =  align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame()
        aligned_color_frame = aligned_frames.get_color_frame()

        # Get depth frame
        #depth_frame = frames.get_depth_frame()
        #color_frame = frames.get_color_frame()

        # Colorize depth frame to jet colormap
        color_color_frame = colorizer.colorize(aligned_color_frame)

        # Convert depth_frame to numpy array to render image in opencv
        color_color_image = np.asanyarray(color_color_frame.get_data())

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(aligned_depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_color_frame.get_data())

        # Show distance from a specific point
        cv2.circle(color_color_image, (point[0], point[1]), 4, (0,0,255),-1)
        dist = aligned_depth_frame.get_distance(int(point[0]), int(point[1]))

        cv2.putText(color_color_image,"{}mm".format(dist),(int(point[0]), int(point[1])),cv2.FONT_HERSHEY_PLAIN,2,(15,255,255),2)

        print("Distance",dist)

        cv2.imshow("Color frame", color_color_image)
        key = cv2.waitKey(1000)
        if key == 27:
            cv2.destroyAllWindows()
            break



finally:
    pass