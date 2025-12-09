"""
Visualization Panel for displaying robot state and trajectories.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QTextEdit, QCheckBox
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg


class VisualizationPanel(QWidget):
    """Panel for visualizing robot state and motion."""
    
    def __init__(self, robot_controller):
        """
        Initialize the visualization panel.
        
        Args:
            robot_controller: RobotController instance
        """
        super().__init__()
        
        self.robot_controller = robot_controller
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Visualization Options
        options_group = QGroupBox("Visualization Options")
        options_layout = QHBoxLayout()
        
        self.show_joints_check = QCheckBox("Show Joints")
        self.show_joints_check.setChecked(True)
        options_layout.addWidget(self.show_joints_check)
        
        self.show_tcp_check = QCheckBox("Show TCP")
        self.show_tcp_check.setChecked(True)
        options_layout.addWidget(self.show_tcp_check)
        
        self.show_trajectory_check = QCheckBox("Show Trajectory")
        self.show_trajectory_check.setChecked(False)
        options_layout.addWidget(self.show_trajectory_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Joint State Plot
        plot_group = QGroupBox("Joint Position Plot")
        plot_layout = QVBoxLayout()
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Position', units='rad')
        self.plot_widget.setLabel('bottom', 'Joint')
        self.plot_widget.setTitle('Current Joint Positions')
        self.plot_widget.showGrid(x=True, y=True)
        
        plot_layout.addWidget(self.plot_widget)
        plot_group.setLayout(plot_layout)
        layout.addWidget(plot_group)
        
        # 3D View placeholder
        view_group = QGroupBox("3D Robot View")
        view_layout = QVBoxLayout()
        
        view_info = QLabel("3D visualization requires RViz2 or additional 3D rendering libraries.\n"
                          "Please use RViz2 for full 3D visualization of the robot.")
        view_info.setWordWrap(True)
        view_info.setAlignment(Qt.AlignCenter)
        view_layout.addWidget(view_info)
        
        self.launch_rviz_btn = QPushButton("Launch RViz2")
        self.launch_rviz_btn.setMinimumHeight(50)
        view_layout.addWidget(self.launch_rviz_btn)
        
        view_group.setLayout(view_layout)
        layout.addWidget(view_group)
        
        # Trajectory Info
        traj_group = QGroupBox("Trajectory Information")
        traj_layout = QVBoxLayout()
        
        self.trajectory_info_text = QTextEdit()
        self.trajectory_info_text.setReadOnly(True)
        self.trajectory_info_text.setMaximumHeight(100)
        self.trajectory_info_text.setPlainText("No trajectory data")
        traj_layout.addWidget(self.trajectory_info_text)
        
        traj_group.setLayout(traj_layout)
        layout.addWidget(traj_group)
    
    def connect_signals(self):
        """Connect signals and slots."""
        self.robot_controller.joint_state_updated.connect(self.update_joint_plot)
        self.robot_controller.trajectory_received.connect(self.update_trajectory_info)
        self.launch_rviz_btn.clicked.connect(self.launch_rviz)
    
    def update_joint_plot(self, joint_states):
        """Update the joint position plot."""
        if not joint_states:
            return
        
        # Extract joint names and positions
        joint_names = sorted(joint_states.keys())
        positions = [joint_states[name]['position'] for name in joint_names]
        
        # Clear and redraw plot
        self.plot_widget.clear()
        
        # Create bar graph
        x = list(range(len(joint_names)))
        bargraph = pg.BarGraphItem(x=x, height=positions, width=0.6, brush='b')
        self.plot_widget.addItem(bargraph)
        
        # Set x-axis labels
        ax = self.plot_widget.getAxis('bottom')
        ax.setTicks([[(i, name) for i, name in enumerate(joint_names)]])
    
    def update_trajectory_info(self, trajectory_msg):
        """Update trajectory information display."""
        info = "Received Trajectory:\n"
        info += "=" * 40 + "\n"
        
        if hasattr(trajectory_msg, 'trajectory') and len(trajectory_msg.trajectory) > 0:
            traj = trajectory_msg.trajectory[0]
            if hasattr(traj, 'joint_trajectory'):
                jt = traj.joint_trajectory
                info += f"Joints: {len(jt.joint_names)}\n"
                info += f"Points: {len(jt.points)}\n"
                if jt.points:
                    duration = jt.points[-1].time_from_start
                    info += f"Duration: {duration.sec}.{duration.nanosec} s\n"
        else:
            info += "No trajectory data available\n"
        
        self.trajectory_info_text.setPlainText(info)
    
    def launch_rviz(self):
        """Launch RViz2 for 3D visualization."""
        import subprocess
        try:
            subprocess.Popen(['rviz2'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            self.trajectory_info_text.setPlainText("RViz2 launched successfully")
        except Exception as e:
            self.trajectory_info_text.setPlainText(f"Failed to launch RViz2: {str(e)}")
