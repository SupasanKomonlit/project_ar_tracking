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

device= client.device( "1a6dded2")

rospy.init_node( "camera" , anonymous=False )

bridge = CvBridge()

pub_image = rospy.Publisher( "test_driver" , Image )

while( not rospy.is_shutdown() ):

    img = device.screencap()

    img = cv2.imdecode( numpy.array(img) , cv2.IMREAD_COLOR )

    # img = cv2.resize( img , None , fx=0.1 , fy=0.1)

    pub_image.publish( bridge.cv2_to_imgmsg( img , "rgb8" ) )
    print "pub image"

    rospy.sleep( 0.05 )