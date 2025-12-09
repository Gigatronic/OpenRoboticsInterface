#!/usr/bin/env python3
"""
Main entry point for the OpenRoboticsInterface application.
"""

import sys
import threading
import rclpy
from rclpy.executors import MultiThreadedExecutor
from PyQt5.QtWidgets import QApplication
from open_robotics_interface.gui.main_window import MainWindow
from open_robotics_interface.ros2_interface.robot_controller import RobotController


def main(args=None):
    """Initialize and run the OpenRoboticsInterface application."""
    # Initialize ROS 2
    rclpy.init(args=args)
    
    # Create ROS 2 robot controller node
    robot_controller = RobotController()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("OpenRoboticsInterface")
    app.setOrganizationName("OpenRobotics")
    
    # Create and show main window
    main_window = MainWindow(robot_controller)
    main_window.show()
    
    # Create ROS 2 executor in a separate thread
    executor = MultiThreadedExecutor()
    executor.add_node(robot_controller)
    
    # Start ROS 2 spinning in background
    ros_thread = threading.Thread(target=executor.spin, daemon=True)
    ros_thread.start()
    
    # Run Qt event loop
    exit_code = app.exec_()
    
    # Cleanup
    robot_controller.destroy_node()
    rclpy.shutdown()
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
