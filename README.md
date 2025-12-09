# OpenRoboticsInterface

A comprehensive graphical interface for controlling robots with ROS 2 and MoveIt 2 support. This application provides an intuitive user interface for robot control, motion planning, programming, and configuration.

## Features

### 🎮 Robot Control
- **Manual Jogging**: Control individual joints with adjustable step sizes
- **Cartesian Control**: Move the robot end-effector in Cartesian space
- **Quick Actions**: Home position, emergency stop, and preset positions
- **Real-time Feedback**: Live joint position and velocity monitoring

### 🤖 Robot Programming
- **Point-to-Point Programming**: Create trajectories by teaching waypoints
- **Program Management**: Save and load robot programs
- **Program Execution**: Run, pause, and stop programmed sequences
- **Visual Program Editor**: Intuitive interface for building motion sequences

### ⚙️ Robot Setup & Configuration
- **ROS 2 Integration**: Configure namespaces and controller connections
- **Robot Configuration**: Support for various robot types and DOF
- **MoveIt 2 Setup**: Configure motion planning parameters
- **Joint Limits**: Set velocity and acceleration constraints
- **System Monitoring**: Real-time system information and diagnostics

### 📊 Visualization
- **Joint State Plotting**: Real-time visualization of joint positions
- **Trajectory Display**: View planned and executed trajectories
- **RViz2 Integration**: Launch and integrate with RViz2 for 3D visualization

## Requirements

### System Requirements
- Ubuntu 22.04 (recommended) or later
- ROS 2 Humble, Iron, or Rolling
- Python 3.8 or later

### ROS 2 Packages
- `rclpy` - ROS 2 Python client library
- `moveit_msgs` - MoveIt 2 message definitions
- `control_msgs` - Control message definitions
- `tf2_ros` - TF2 ROS Python bindings
- `sensor_msgs`, `geometry_msgs`, `trajectory_msgs` - Standard ROS 2 messages

### Python Packages
- `PyQt5` - GUI framework
- `pyqtgraph` - Plotting and visualization
- `numpy` - Numerical operations
- `pyyaml` - Configuration file parsing

## Installation

### 1. Install ROS 2
Follow the official ROS 2 installation guide for your distribution:
- [ROS 2 Humble Installation](https://docs.ros.org/en/humble/Installation.html)

### 2. Install MoveIt 2
```bash
sudo apt update
sudo apt install ros-${ROS_DISTRO}-moveit
```

### 3. Clone and Build
```bash
# Create a ROS 2 workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone the repository
git clone https://github.com/Gigatronic/OpenRoboticsInterface.git

# Install Python dependencies
cd OpenRoboticsInterface
pip install -r requirements.txt

# Build the workspace
cd ~/ros2_ws
colcon build --packages-select open_robotics_interface

# Source the workspace
source install/setup.bash
```

## Usage

### Launch the GUI
```bash
# Source ROS 2 and workspace
source /opt/ros/${ROS_DISTRO}/setup.bash
source ~/ros2_ws/install/setup.bash

# Run the GUI
ros2 run open_robotics_interface robot_gui
```

### Launch with Custom Configuration
```bash
# Using launch file
ros2 launch open_robotics_interface robot_interface.launch.py config:=/path/to/config.yaml

# With namespace
ros2 launch open_robotics_interface robot_interface.launch.py namespace:=/robot1
```

### Connect to Your Robot
1. Ensure your robot is running and publishing joint states on `/joint_states`
2. Verify that a joint trajectory controller is available
3. Launch the GUI - it will automatically detect and connect to the robot
4. Check the "Setup" tab for connection status and configuration

## GUI Overview

### Control Tab
- **Joint Control**: Manually jog individual joints
- **Current Positions**: Real-time display of all joint positions
- **Quick Actions**: Home, stop, and preset positions

### Programming Tab
- **Program Points**: Add current positions as waypoints
- **Program List**: View and manage programmed sequences
- **Execution Controls**: Run, pause, and stop programs
- **Program Management**: Save and load programs to/from disk

### Setup Tab
- **Connection Settings**: Configure ROS 2 namespace and controllers
- **Robot Configuration**: Set robot type and degrees of freedom
- **MoveIt 2 Settings**: Configure motion planner and planning parameters
- **Joint Limits**: Set velocity and acceleration constraints
- **System Information**: View connected joints and system status

### Visualization Tab
- **Joint Position Plot**: Real-time bar graph of joint positions
- **Trajectory Information**: Details about planned trajectories
- **RViz2 Integration**: Launch RViz2 for 3D visualization

## Configuration

The application uses YAML configuration files. Default configuration is in `config/default_config.yaml`.

Example configuration:
```yaml
ros2:
  namespace: ""
  controller_name: "joint_trajectory_controller"

robot:
  type: "generic_6dof"
  degrees_of_freedom: 6
  planning_group: "manipulator"

moveit:
  enabled: true
  planner: "RRTConnect"
  planning_time: 5.0

joint_limits:
  max_velocity: 1.0
  max_acceleration: 2.0
```

## Supported Robot Types

The interface is designed to work with any ROS 2 compatible robot that provides:
- Joint state information on `/joint_states`
- A joint trajectory controller (e.g., `joint_trajectory_controller`)
- Optional: MoveIt 2 configuration for motion planning

Tested with:
- Universal Robots (UR5, UR10)
- Franka Emika Panda
- Generic 6-DOF and 7-DOF manipulators

## Development

### Project Structure
```
OpenRoboticsInterface/
├── open_robotics_interface/
│   ├── gui/                    # GUI components
│   │   ├── main_window.py      # Main application window
│   │   ├── control_panel.py    # Robot control interface
│   │   ├── programming_panel.py # Programming interface
│   │   ├── setup_panel.py      # Configuration interface
│   │   └── visualization_panel.py # Visualization interface
│   ├── ros2_interface/         # ROS 2 integration
│   │   └── robot_controller.py # Robot controller node
│   ├── utils/                  # Utility functions
│   └── main.py                 # Application entry point
├── config/                     # Configuration files
├── launch/                     # Launch files
├── package.xml                 # ROS 2 package manifest
├── setup.py                    # Python package setup
└── requirements.txt            # Python dependencies
```

### Running Tests
```bash
cd ~/ros2_ws
colcon test --packages-select open_robotics_interface
```

## Troubleshooting

### GUI doesn't start
- Ensure PyQt5 is installed: `pip install PyQt5`
- Check ROS 2 environment is sourced: `source /opt/ros/${ROS_DISTRO}/setup.bash`

### Robot not connecting
- Verify robot is publishing on `/joint_states`: `ros2 topic echo /joint_states`
- Check controller name matches your robot's controller
- Review connection settings in the Setup tab

### MoveIt 2 not working
- Ensure MoveIt 2 is installed: `sudo apt install ros-${ROS_DISTRO}-moveit`
- Verify MoveIt 2 is running: `ros2 node list | grep move_group`
- Check planning group name in configuration

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ROS 2 and MoveIt 2
- GUI framework: PyQt5
- Visualization: pyqtgraph

## Support

For questions and support, please open an issue on GitHub.