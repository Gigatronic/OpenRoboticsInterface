"""
ROS 2 Robot Controller Node.
Handles communication with robot hardware and MoveIt 2.
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped, Pose
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
from moveit_msgs.msg import DisplayTrajectory, RobotState
from moveit_msgs.srv import GetPositionIK, GetPositionFK
from std_msgs.msg import String
from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class RobotController(Node, QObject):
    """ROS 2 node for controlling robot through MoveIt 2 and direct commands."""
    
    # Qt signals for GUI updates
    joint_state_updated = pyqtSignal(dict)
    robot_status_updated = pyqtSignal(str)
    trajectory_received = pyqtSignal(object)
    
    def __init__(self):
        """Initialize the robot controller node."""
        Node.__init__(self, 'robot_controller')
        QObject.__init__(self)
        
        self.get_logger().info('Initializing Robot Controller...')
        
        # Robot state
        self.current_joint_state = {}
        self.current_pose = None
        self.robot_connected = False
        
        # Joint names (will be populated from joint_states)
        self.joint_names = []
        
        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        self.display_trajectory_sub = self.create_subscription(
            DisplayTrajectory,
            '/move_group/display_planned_path',
            self.display_trajectory_callback,
            10
        )
        
        # Publishers
        self.command_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.status_pub = self.create_publisher(
            String,
            '/robot_status',
            10
        )
        
        # Action clients
        self.follow_joint_trajectory_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )
        
        # Service clients
        self.ik_client = self.create_client(
            GetPositionIK,
            '/compute_ik'
        )
        
        self.fk_client = self.create_client(
            GetPositionFK,
            '/compute_fk'
        )
        
        self.get_logger().info('Robot Controller initialized')
        self.publish_status('Robot Controller Ready')
    
    def joint_state_callback(self, msg):
        """Process incoming joint state messages."""
        if not self.joint_names:
            self.joint_names = list(msg.name)
            self.get_logger().info(f'Detected joints: {self.joint_names}')
        
        # Update current joint state
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.current_joint_state[name] = {
                    'position': msg.position[i],
                    'velocity': msg.velocity[i] if i < len(msg.velocity) else 0.0,
                    'effort': msg.effort[i] if i < len(msg.effort) else 0.0
                }
        
        self.robot_connected = True
        # Emit signal for GUI update
        self.joint_state_updated.emit(self.current_joint_state.copy())
    
    def display_trajectory_callback(self, msg):
        """Process planned trajectory from MoveIt 2."""
        self.get_logger().info('Received planned trajectory')
        self.trajectory_received.emit(msg)
    
    def publish_status(self, status_msg):
        """Publish status message."""
        msg = String()
        msg.data = status_msg
        self.status_pub.publish(msg)
        self.robot_status_updated.emit(status_msg)
    
    def move_joints(self, joint_positions, duration=2.0):
        """
        Move robot joints to specified positions.
        
        Args:
            joint_positions: Dictionary mapping joint names to target positions
            duration: Time to complete the movement (seconds)
        """
        if not self.joint_names:
            self.get_logger().warn('No joint names available')
            return False
        
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        
        point = JointTrajectoryPoint()
        point.positions = [
            joint_positions.get(name, self.current_joint_state.get(name, {}).get('position', 0.0))
            for name in self.joint_names
        ]
        point.time_from_start.sec = int(duration)
        point.time_from_start.nanosec = int((duration % 1) * 1e9)
        
        trajectory.points.append(point)
        
        self.command_pub.publish(trajectory)
        self.get_logger().info(f'Sent joint trajectory command')
        return True
    
    def jog_joint(self, joint_name, delta):
        """
        Jog a single joint by a delta amount.
        
        Args:
            joint_name: Name of the joint to jog
            delta: Amount to move (radians)
        """
        if joint_name not in self.current_joint_state:
            self.get_logger().warn(f'Joint {joint_name} not found')
            return False
        
        current_pos = self.current_joint_state[joint_name]['position']
        new_positions = {joint_name: current_pos + delta}
        
        return self.move_joints(new_positions, duration=0.5)
    
    def get_current_joint_positions(self):
        """Get current joint positions as dictionary."""
        return {
            name: state['position']
            for name, state in self.current_joint_state.items()
        }
    
    def get_joint_names(self):
        """Get list of joint names."""
        return self.joint_names.copy()
    
    def is_connected(self):
        """Check if robot is connected."""
        return self.robot_connected
    
    def home_robot(self):
        """Move robot to home position (all joints at 0)."""
        home_positions = {name: 0.0 for name in self.joint_names}
        return self.move_joints(home_positions, duration=3.0)
