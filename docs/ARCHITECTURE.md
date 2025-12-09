# OpenRoboticsInterface Architecture

## Overview

OpenRoboticsInterface is designed as a modular application with clear separation between the GUI layer, ROS 2 integration layer, and utility functions.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Application                          │
│                     (main.py)                                │
└────────────────┬───────────────────────────┬─────────────────┘
                 │                           │
        ┌────────▼────────┐         ┌────────▼──────────┐
        │   GUI Layer     │         │  ROS 2 Interface  │
        │   (PyQt5)       │◄───────►│   (rclpy)         │
        └────────┬────────┘         └────────┬──────────┘
                 │                           │
    ┌────────────┼────────────┐             │
    │            │            │             │
┌───▼───┐  ┌───▼───┐  ┌─────▼──┐    ┌─────▼──────────┐
│Control│  │Program│  │Setup   │    │Robot Controller│
│Panel  │  │Panel  │  │Panel   │    │     Node       │
└───────┘  └───────┘  └────┬───┘    └─────┬──────────┘
                            │              │
                      ┌─────▼──┐    ┌──────▼──────┐
                      │Visual  │    │   MoveIt 2  │
                      │Panel   │    │   Interface │
                      └────────┘    └─────────────┘
```

## Module Description

### Main Application (`main.py`)
- Entry point for the application
- Initializes ROS 2 context
- Creates Qt application instance
- Manages main event loop
- Handles application lifecycle

### GUI Layer (`gui/`)

#### Main Window (`main_window.py`)
- Primary application window
- Tab-based interface
- Menu bar and status bar
- Connection status monitoring
- Orchestrates all GUI panels

#### Control Panel (`control_panel.py`)
- Manual robot control
- Joint jogging interface
- Real-time joint position display
- Quick action buttons (home, stop)
- Cartesian control (future)

#### Programming Panel (`programming_panel.py`)
- Waypoint teaching interface
- Program point management
- Trajectory execution controls
- Program save/load functionality
- Program visualization

#### Setup Panel (`setup_panel.py`)
- ROS 2 connection configuration
- Robot type selection
- MoveIt 2 configuration
- Joint limit settings
- System information display

#### Visualization Panel (`visualization_panel.py`)
- Real-time joint state plotting
- Trajectory visualization
- RViz2 integration
- 3D robot model (via RViz2)

### ROS 2 Interface (`ros2_interface/`)

#### Robot Controller (`robot_controller.py`)
- ROS 2 node for robot communication
- Joint state subscriber
- Trajectory publisher
- Action client for trajectory execution
- Service clients for IK/FK
- Qt signal emission for GUI updates

### Utilities (`utils/`)
- Configuration management
- Coordinate transformations
- Helper functions

## Data Flow

### Robot State Updates
1. Robot publishes joint states → `/joint_states`
2. RobotController receives states
3. RobotController emits Qt signal
4. GUI panels update displays

### Motion Commands
1. User interacts with GUI
2. GUI calls RobotController method
3. RobotController publishes trajectory
4. Robot executes motion
5. Joint states update (feedback loop)

### MoveIt 2 Integration
1. User requests motion plan
2. RobotController calls MoveIt 2 service
3. MoveIt 2 computes trajectory
4. Trajectory displayed in GUI
5. User approves execution
6. RobotController executes trajectory

## Communication Patterns

### Qt Signals and Slots
- Used for GUI updates from ROS 2 thread
- Thread-safe communication
- Decouples ROS 2 from Qt event loop

### ROS 2 Topics
- `/joint_states`: Robot joint state feedback
- `/joint_trajectory`: Joint trajectory commands
- `/robot_status`: Status messages

### ROS 2 Actions
- `/follow_joint_trajectory`: Trajectory execution

### ROS 2 Services
- `/compute_ik`: Inverse kinematics
- `/compute_fk`: Forward kinematics
- MoveIt 2 planning services

## Threading Model

```
Main Thread (Qt)
├── GUI Event Loop
├── User Interactions
└── Display Updates

ROS 2 Thread
├── Subscriber Callbacks
├── Publisher/Action Calls
└── Service Requests
```

The application uses multi-threading to keep GUI responsive:
- Main thread runs Qt event loop
- Separate thread runs ROS 2 executor
- Qt signals bridge between threads

## Configuration

Configuration is loaded from YAML files:
- Default configuration in `config/default_config.yaml`
- User can specify custom configuration
- Runtime configuration changes via Setup panel

## Extension Points

The architecture supports easy extension:

1. **New GUI Panels**: Add tabs to main window
2. **Custom Robot Support**: Update configuration files
3. **Additional ROS 2 Topics**: Extend robot controller
4. **New Planning Algorithms**: Configure MoveIt 2
5. **Custom Visualizations**: Add to visualization panel

## Dependencies

### Required
- ROS 2 (Humble or later)
- Python 3.8+
- PyQt5
- rclpy
- sensor_msgs, geometry_msgs, trajectory_msgs

### Optional
- MoveIt 2 (for motion planning)
- pyqtgraph (for visualization)
- RViz2 (for 3D visualization)

## Design Principles

1. **Modularity**: Clear separation of concerns
2. **Extensibility**: Easy to add features
3. **User-Friendly**: Intuitive interface
4. **Real-Time**: Responsive to robot feedback
5. **Safety**: Emergency stop and status monitoring
6. **Compatibility**: Works with standard ROS 2 robots
