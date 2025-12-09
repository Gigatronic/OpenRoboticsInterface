#!/usr/bin/env python3
"""
Simple robot simulator for testing OpenRoboticsInterface without real hardware.
Publishes dummy joint states that the GUI can connect to.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Time
import math


class RobotSimulator(Node):
    """Simulates a 6-DOF robot by publishing joint states."""
    
    def __init__(self):
        super().__init__('robot_simulator')
        
        # Create publisher
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        
        # Create timer for publishing at 50Hz
        self.timer = self.create_timer(0.02, self.publish_joint_states)
        
        # Joint configuration
        self.joint_names = [
            'joint_1',
            'joint_2', 
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6'
        ]
        
        # Initial positions
        self.positions = [0.0] * 6
        self.velocities = [0.0] * 6
        self.efforts = [0.0] * 6
        
        # Animation parameters
        self.time = 0.0
        
        self.get_logger().info('Robot Simulator started')
        self.get_logger().info(f'Publishing joint states for: {self.joint_names}')
    
    def publish_joint_states(self):
        """Publish simulated joint states."""
        msg = JointState()
        
        # Set timestamp
        now = self.get_clock().now()
        msg.header.stamp = now.to_msg()
        msg.header.frame_id = ''
        
        # Animate joints (simple sine wave)
        self.time += 0.02
        amplitude = 0.5
        
        for i in range(len(self.joint_names)):
            # Create different phase offsets for each joint
            phase = i * math.pi / 3
            self.positions[i] = amplitude * math.sin(self.time + phase)
            self.velocities[i] = amplitude * math.cos(self.time + phase)
        
        msg.name = self.joint_names
        msg.position = self.positions
        msg.velocity = self.velocities
        msg.effort = self.efforts
        
        self.publisher.publish(msg)


def main(args=None):
    """Run the robot simulator."""
    rclpy.init(args=args)
    
    simulator = RobotSimulator()
    
    try:
        rclpy.spin(simulator)
    except KeyboardInterrupt:
        pass
    finally:
        simulator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
