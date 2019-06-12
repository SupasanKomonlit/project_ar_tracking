#!/usr/bin/env python2
# FILE			: filter_bag.py
# AUTHOR		: K.Supasan
# CREATE ON		: 2019, June 12 (UTC+0)
# MAINTAINER	: K.Supasan

# README

# REFERENCE

from __future__ import print_function

import rosbag


name_bag_input = "original_bag_06_07.bag"
name_bag_output = "new_bag_06_07.bag"

bag_read = rosbag.Bag( name_bag_input )
bag_write = rosbag.Bag( name_bag_output , 'w' )

for topic , msg , t in bag_read.read_messages( topics = [ '/tf' , '/tf_static' , '/rayfin/image' , '/rayfin/camera_info']):
    if( topic == '/tf' ):
        if( ( msg.transforms[0].header.frame_id == "rayfin_optical_frame" 
            and msg.transforms[0].child_frame_id == "ar_marker_0" ) 
            or ( msg.transforms[0].header.frame_id == "ar_marker_0" 
            and msg.transforms[0].child_frame_id == "base_marker" ) 
            or ( msg.transforms[0].header.frame_id == "base_marker"
            and msg.transforms[0].child_frame_id == "base_cage" ) ):
            print( "Remove {:s} parent frame is {:s} and child_frame_id is {:s}".format(
                topic
                , msg.transforms[0].header.frame_id
                , msg.transforms[0].child_frame_id ) )
        else:
            bag_write.write( topic , msg , t = msg.transforms[0].header.stamp )
            temp_time = msg.transforms[0].header.stamp
    elif( topic == '/tf_static' ):
        bag_write.write( topic , msg , t = temp_time )
    else:
        bag_write.write( topic , msg , t = msg.header.stamp )
        temp_time = msg.header.stamp

bag_read.close()
bag_write.close()
