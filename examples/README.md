# OpenRoboticsInterface Examples

This directory contains example scripts and configurations for testing and demonstrating the OpenRoboticsInterface.

## Robot Simulator

The `robot_simulator.py` script provides a simple simulated robot for testing the GUI without real hardware.

### Usage

1. In one terminal, run the simulator:
```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
python3 robot_simulator.py
```

2. In another terminal, launch the GUI:
```bash
source /opt/ros/${ROS_DISTRO}/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run open_robotics_interface robot_gui
```

The GUI should connect to the simulator and display the animated joint states.

### What it does

- Publishes joint states for a 6-DOF robot
- Animates joints with simple sine wave motion
- Provides realistic topic structure for testing

## Additional Examples

More examples will be added for:
- Custom robot configurations
- Pre-programmed motion sequences  
- Integration with specific robot models
