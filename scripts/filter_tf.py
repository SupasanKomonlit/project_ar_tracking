#!/usr/bin/env python2
# FILE			: filter_tf.py
# AUTHOR		: K.Supasan
# CREATE ON		: 2019, June 14 (UTC+0)
# MAINTAINER	: K.Supasan

# README
#   This code I will design to manage filter of tf message by receive tf on tf listener
#   and I will broadcast on tf broadcast

# REFERENCE
#   ref1    : http://docs.ros.org/melodic/api/tf/html/python/tf_python.html#transformlistener
#   ref2    : http://wiki.ros.org/rospy/Overview/Parameter%20Server
#   ref3    : http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20listener%20%28Python%29
#   ref4    : http://wiki.ros.org/tf/Overview/Exceptions
#   ref5    : http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20broadcaster%20%28Python%29

import tf
import rospy
import numpy
import roslib
from syrena_utils.window import Window

class TFFilter:

    # Function __init__ will manage about create varable of this object
    def __init__( self ):

        self.time_duration = rospy.get_param( "time_duration" , 1.0 )

        self.parent_frame = rospy.get_param( "old_parent_frame" , "rayfin_optical_frame" )

        self.old_child_frame = rospy.get_param( "old_child_frame" , "ar_pose_marker6" )

        self.new_child_frame = rospy.get_param( "new_child_frame" , "filter_marker" )

        self.listener = tf.TransformListener()

        self.sender = tf.TransformBroadcaster()

        self.buffer = Window( duration = self.time_duration )

        # This variable use to protect about send data which ever broadcaster
        self.new_data = False 

    # This function will call or listen tf data 
    def add_data( self ):
        # We will use loop to manage about that you will see warning when I can't get tf for you
        while( not rospy.is_shutdown() ):
            try:
                original = self.listener.lookupTransform( self.parent_frame 
                    , self.old_child_frame 
                    , rospy.Time(0) )
            except ( tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException ):
                rospy.logerr( "Waiting for tf value 0.5 secs from %s to %s" 
                    , self.parent_frame 
                    , self.old_child_frame )
                rospy.sleep( 0.5 )
                continue
            self.buffer.add( original )
            break

    # This function will broadcast loop of tf from parent_frame to new_child_frame
    def broadcast_loop( self ):
        while( not rospy.is_shutdown() ):
            self.add_data()
            self.filter_function()
            if( self.new_data ):
                self.sender.sendTransform( self.linear 
                    , self.quaternion 
                    , rospy.get_rosTime()
                    , self.new_child_frame 
                    , self.parent_frame )

    # Below function of filter_function will get data and assing variable for transformation
    def filter_function( self ):
        # Data will get ( linear , rotation )
        #   linear is tuple of x y z axis
        #   rotation is tuple of quaternion
        raw_data = self.buffer.get_data()

if __name__ == '__main__' :

    rospy.init_node( "filter_tf" )

    tffilter = TFFilter()

    tffilter.broadcast_loop()
