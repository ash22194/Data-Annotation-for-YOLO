#! /usr/bin/python
# Copyright (c) 2015, Rethink Robotics, Inc.

# Using this CvBridge Tutorial for converting
# ROS images to OpenCV2 images
# http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

# Using this OpenCV2 tutorial for saving Images:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
# Handle command line arguments
import sys
import argparse


# Instantiate CvBridge
bridge = CvBridge()

# Number of images to save
global nImages

# Start count i.e Index of the first image saved
global sCount

# Current count i.e. numebr of images saved
global cCount

# Directory to save
global dirToSave

## Fix the termination condition!!

def image_callback(msg):
    print("Received an image!")
    global cCount
    global dirToSave
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        # Save your OpenCV2 image as a jpeg 
        cv2.imwrite(dirToSave + '/' + str(sCount+cCount) + '.jpg', cv2_img)
        print("Image %d Saved!"%(cCount))
        cCount+=1

def main(startCount,numImages,directory):
    global sCount
    global nImages
    global cCount
    global dirToSave

    cCount = 0
    sCount = startCount
    nImages = numImages
    dirToSave = directory

    rospy.init_node('image_listener')
    # Define your image topic
    image_topic = "/pepper_robot/camera/front/image_rect_color"
    # Set up your subscriber and define its callback
    rospy.Subscriber(image_topic, Image, image_callback)
    # Spin until ctrl + c
    # rospy.spin()
    while not rospy.core.is_shutdown():
        if (cCount>=nImages):
            rospy.signal_shutdown('Requested number of images saved')
        rospy.rostime.wallsleep(0.1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-sc', type=float, default=0, help='Index of the first image')
    parser.add_argument('-ni', type=float, default=10, help='Number of images to save')
    parser.add_argument('-dir', type=str, default='', help='Path of the directory to save images to')

    args = parser.parse_args()
    main(startCount=args.sc,numImages=args.ni,directory=args.dir)