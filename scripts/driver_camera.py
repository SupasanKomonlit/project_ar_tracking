#!/usr/bin/env python
# FILE			: driver_camera.py
# AUTHOR		: K.Supasan
# CREATE ON		: 2019, June 04 (UTC+0)
# MAINTAINER	: K.Supasan

# README

# REFERENCE

from adb.client import Client as AdbClient

import rospy

import cv2

import numpy

from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError

client = AdbClient( host="127.0.0.1" , port=5037 )

device= client.device( "192.168.0.34:5555")

rospy.init_node( "camera" , anonymous=False )

bridge = CvBridge()

pub_image = rospy.Publisher( "/rayfin/image" , Image , queue_size=10 )

count = 0

# my ip 192.168.0.221

while( not rospy.is_shutdown() ):

    time_now = rospy.get_rostime()

    img = device.screencap()

    img = cv2.imdecode( numpy.array(img) , cv2.IMREAD_COLOR )

    img = cv2.resize( img , None , fx=0.5 , fy=0.5)

    msg = bridge.cv2_to_imgmsg( img , "bgr8" )
   
    print time_now 
    msg.header.stamp = time_now
    msg.header.frame_id = "rayfin_optical_frame"

    pub_image.publish( msg )
    print "Send!"
    rospy.sleep( 0.05 )
