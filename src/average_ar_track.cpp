// FILE			: average_ar_track.cpp
// AUTHOR		: K.Supasan
// CREATE ON	: 2019, May 29 (UTC+0)
// MAINTAINER	: K.Supasan

// MACRO DETAIL

// README

// REFERENCE

// MACRO SET

// MACRO CONDITION

#include    <iostream>

#include    <cmath>

#include    <ros/ros.h>

#include    <array>

#include    <ar_track_alvar_msgs/AlvarMarkers.h>

template< unsigned int size >
class specific_sub 
{

    public:
        specific_sub( int mark_id , bool* updated )
        {
            (this->buffer).fill(0);
            this->target_mark = mark_id;
            this->sum_buffer = 0;
            this->point = 0;
            this->ptr_updated = updated;
        } // function constructor

        void callback( const ar_track_alvar_msgs::AlvarMarkers& msg )
        {
            for( unsigned int run = 0 ; run < msg.markers.size() ; run++ )
            {
                if( msg.markers[run].id == this->target_mark )
                {
                    geometry_msgs::Point distance = msg.markers[run].pose.pose.position;
                    this->average_buffer( sqrt ( 
                            pow( distance.x , 2 ) 
                            + pow( distance.y , 2 )
                            + pow( distance.z , 2 ) ) );
                    *(this->ptr_updated) = true;
                }
            }    
        } // function callback

        double average_buffer( double input )
        {
            this->sum_buffer -= (this->buffer)[ this->point ]; 
            (this->buffer)[ this->point ] = input;
            this->sum_buffer += input;
            this->point = ( this->point  + 1 ) % size;
            return this->get_result();
        } // function average_buffer

        double get_result()
        {
            return this->sum_buffer / size;
        }

    private:
        int target_mark;
        double sum_buffer;
        unsigned int point;
        std::array< double , size > buffer; 
        bool* ptr_updated;

}; // end process declare object 

int main( int argv , char** argc )
{

    ros::init( argv , argc , "average_ar_track" );

    ros::NodeHandle ph("~"); // param handle form launch
    ros::NodeHandle nh("");

    std::string input_topic;
    std::string output_float64;
    int mark_id;

    (void)ph.param< int >("mark_id" , mark_id , (int)8 );
    (void)ph.param< std::string >("input_topic" , input_topic , "/ar_pose_marker" );
    (void)ph.param< std::string >("output_float64" , output_float64 , "/distance_marker" );

    std::cout   << "Focus on mark id is " << mark_id 
                << "\nOn topic " << input_topic << "\n";

    unsigned int point = 0;
    bool updated = false;

    specific_sub< 10 > helper_sub( mark_id , &updated );
   
    ros::Subscriber sub = nh.subscribe( input_topic ,1 ,&specific_sub< 10 >::callback, &helper_sub);
 
    ros::Rate rate(30);

    // sleep for check process
    unsigned int count = 0;
    while( nh.ok() && count < 60 )
    {
        count++;
        rate.sleep();
    }

    // loop calculate
    while( nh.ok() )
    {
        rate.sleep();
        if( updated )
        {
            std::cout   << "Result distance is " << helper_sub.get_result();
            updated = false;
        }
        ros::spinOnce();
    }

    ros::shutdown();
}
