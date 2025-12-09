#!/usr/bin/env python3
"""
Launch file for OpenRoboticsInterface.
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    """Generate launch description for the robot interface."""
    
    # Declare arguments
    config_arg = DeclareLaunchArgument(
        'config',
        default_value=os.path.join(
            get_package_share_directory('open_robotics_interface'),
            'config',
            'default_config.yaml'
        ),
        description='Path to configuration file'
    )
    
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Robot namespace'
    )
    
    # Robot GUI node
    robot_gui_node = Node(
        package='open_robotics_interface',
        executable='robot_gui',
        name='robot_gui',
        namespace=LaunchConfiguration('namespace'),
        output='screen',
        parameters=[LaunchConfiguration('config')],
        emulate_tty=True
    )
    
    return LaunchDescription([
        config_arg,
        namespace_arg,
        robot_gui_node
    ])
