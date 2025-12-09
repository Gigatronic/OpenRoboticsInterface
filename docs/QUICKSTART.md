# Quick Start Guide

This guide will help you get OpenRoboticsInterface up and running quickly.

## Prerequisites

Before you begin, ensure you have:
- Ubuntu 22.04 (or compatible Linux distribution)
- ROS 2 Humble or later installed
- Python 3.8 or later

## Installation Steps

### 1. Install System Dependencies

```bash
# Update package list
sudo apt update

# Install ROS 2 (if not already installed)
# Follow: https://docs.ros.org/en/humble/Installation.html

# Install Python dependencies
sudo apt install python3-pip

# Install PyQt5
pip install PyQt5 pyqtgraph numpy pyyaml
```

### 2. Set Up ROS 2 Workspace

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone the repository
git clone https://github.com/Gigatronic/OpenRoboticsInterface.git

# Go back to workspace root
cd ~/ros2_ws

# Source ROS 2
source /opt/ros/humble/setup.bash

# Install dependencies
rosdep install --from-paths src --ignore-src -r -y

# Build the package
colcon build --packages-select open_robotics_interface

# Source the workspace
source install/setup.bash
```

### 3. Test Without a Robot

You can test the GUI without real hardware using the provided simulator:

```bash
# Terminal 1: Run the simulator
cd ~/ros2_ws/src/OpenRoboticsInterface/examples
python3 robot_simulator.py
```

```bash
# Terminal 2: Launch the GUI
source ~/ros2_ws/install/setup.bash
ros2 run open_robotics_interface robot_gui
```

You should see the GUI window open and connect to the simulated robot!

## Using with a Real Robot

### 1. Ensure Your Robot is Running

Your robot should:
- Publish joint states on `/joint_states` topic
- Have a joint trajectory controller running
- (Optional) Have MoveIt 2 configured

Verify with:
```bash
# Check joint states
ros2 topic echo /joint_states

# List available controllers
ros2 control list_controllers
```

### 2. Launch the Interface

```bash
source ~/ros2_ws/install/setup.bash
ros2 run open_robotics_interface robot_gui
```

### 3. Configure Connection (if needed)

If your robot uses a different namespace or controller:
1. Open the "Setup" tab
2. Update the namespace and controller name
3. Click "Reconnect"

## Basic Usage

### Control Tab

**Jogging Joints:**
1. Select a joint from the dropdown
2. Set the jog step size (degrees)
3. Click "Jog -" or "Jog +" to move the joint

**Quick Actions:**
- Click "Home Position" to move to zero position
- Click "Stop Motion" for emergency stop

### Programming Tab

**Creating a Program:**
1. Move robot to desired position (using Control tab)
2. Click "Add Current Position"
3. Give the point a name
4. Repeat for additional points
5. Click "Run Program" to execute

### Setup Tab

**Viewing System Info:**
- Check connection status
- View detected joints
- See ROS 2 node information

**Configuring Robot:**
- Select robot type
- Set degrees of freedom
- Configure MoveIt 2 settings

### Visualization Tab

**Viewing Joint States:**
- Real-time bar graph shows current joint positions
- Updated automatically as robot moves

**3D Visualization:**
- Click "Launch RViz2" to open 3D viewer
- Configure RViz2 to show robot model and planning scene

## Troubleshooting

### GUI Won't Start

**Error: "No module named 'PyQt5'"**
```bash
pip install PyQt5
```

**Error: "No module named 'rclpy'"**
```bash
# Source ROS 2
source /opt/ros/humble/setup.bash
# Source workspace
source ~/ros2_ws/install/setup.bash
```

### Robot Not Connecting

**Check if robot is publishing:**
```bash
ros2 topic list | grep joint_states
ros2 topic echo /joint_states
```

**Verify controller:**
```bash
ros2 control list_controllers
```

**Check namespace:**
- If your robot uses a namespace (e.g., `/robot1`), configure it in the Setup tab

### Performance Issues

**GUI is slow:**
- Reduce update rate in Setup tab
- Close unused applications
- Check CPU usage with `top` or `htop`

**ROS 2 messages delayed:**
- Check network connection (if robot is remote)
- Verify ROS 2 DDS settings
- Check for message queue overflow

## Next Steps

- Read the full [README](../README.md) for detailed features
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- Explore example programs in the `examples/` directory
- Configure your robot in `config/default_config.yaml`

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review ROS 2 and robot logs
3. Open an issue on GitHub with:
   - Your ROS 2 version
   - Error messages
   - Steps to reproduce

## Tips for Success

1. **Always test with the simulator first** before using real hardware
2. **Use emergency stop** if robot behaves unexpectedly
3. **Start with small jog steps** when manually controlling
4. **Save programs frequently** to avoid losing work
5. **Keep RViz2 open** for visual feedback during operation

Happy robot programming! 🤖
