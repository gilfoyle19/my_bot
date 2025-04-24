import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('my_bot'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher', #<--- package name
        executable='robot_state_publisher', #executable means the name of the node
        output='screen',         
        parameters=[params]
    )




    # Launch the robot_state_publisher node
    # and pass the robot description to it
    # The robot description is a parameter that contains the URDF model of the robot
    # The robot_state_publisher node will publish the robot's state to the /tf topic
    # The robot_state_publisher node will also publish the robot's joint states to the /joint_states topic
    return LaunchDescription([ #<--- LaunchDescription is a class that contains the launch description
        DeclareLaunchArgument(
            'use_sim_time',               #<--- Declare a launch argument
            default_value='false',        #false means use the real time clock
            description='Use sim time if true'), #means use the simulation clock

        node_robot_state_publisher        #<--- Launch the robot_state_publisher node
    ])
