#!/usr/bin/env python
# FILE			: publish_camera_info.py
# AUTHOR		: K.Supasan
# CREATE ON		: 2019, June 06 (UTC+0)
# MAINTAINER	: K.Supasan

# README
#   This code not want to full path for standard use. This code support param launch file is
#   ROS operating system

# REFERENCE
#   ref01   : https://pyyaml.org/wiki/PyYAMLDocumentation
#   ref02   : http://answers.ros.org/question/169866/load-yaml-with-code/

import rospy

from yaml import load

from sensor_msgs import CameraInfo

class PublishCameraInfo:

    def __init__( self ):

        self.name = rospy.get_name()
        if( rospy.has_param( "name" ) ):
            self.name = rospy.get_param( "name" )


        self.full_path_yaml = ""
        if( rospy.has_param('yaml') ):
            self.full_path_yaml = rospy.get_param('yaml')

        self.message = CameraInfo

        topic_publish = '/' + self.name + '/camera_info'
        self.publisher = rospy.Publisher( topic_publish , CameraInfo , queue_size = 10 )

    def set_full_path( self , full_path ):
        self.full_path_yaml = full_path

    def load_data( self ):

        yaml_file = open( self.full_path_yaml , 'r' )
        yaml_data = load( yaml_file )
        yaml_file.close()

        self.message.header.frame_id = yaml_data[ 'camera_name']
        self.message.height = yaml_data[ 'image_height' ]
        self.message.width = yaml_data[ 'image_width' ]
        self.message.distortion_model = yaml_data[ 'distortion_model' ]
        self.message.D = yaml_data[ 'distortion_coefficients' ][ 'data' ]
        self.message.K = yaml_data[ 'camera_matrix' ][ 'data' ]
        self.message.R = yaml_data[ 'rectification_matrix' ][ 'data' ]
        self.message.P = yaml_data[ 'distortion_model' ][ 'data' ]

# Below part is 0 because don't have this part in basic calibration of ROS modle
        self.message.binning_x = 0
        self.message.binning_y = 0
        self.message.roi.x_offset = 0
        self.message.roi.y_offset = 0
        self.message.roi.height = 0
        self.message.roi.width = 0
        self.message.roi.dorectify = False

    def spin_publish( self ):
        while( not rospy.is_shutdown() ):
            rospy.sleep( 0.1 )
            self.message.header.stamp = rospy.get_time()

            self.publisher=publish( self.message )

if __name__=="__main__":
    pub_camera_info = PublishCameraInfo()

    rospy.init_node( "pub_camera_info" , anonymous=True )

    pub_camera_info.load_data()

    pub_camera_info.spin_publish()
