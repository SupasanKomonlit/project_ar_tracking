cmake_minimum_required( VERSION 2.8.3 )

project( project_ar_tracking )

find_package( catkin REQUIRED COMPONENTS roscpp ar_track_alvar_msgs geometry_msgs )

catkin_package(
    CATKIN_DEPENDS roscpp ar_track_alvar_msgs geometry_msgs
)

include_directories(
    ${catkin_INCLUDE_DIRS}
)

add_executable( average_ar_track 
    src/average_ar_track
)
target_link_libraries( average_ar_track ${catkin_LIBRARIES})
