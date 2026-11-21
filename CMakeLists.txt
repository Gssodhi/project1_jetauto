cmake_minimum_required(VERSION 3.0.2)
project(project1_jetauto)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  std_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
