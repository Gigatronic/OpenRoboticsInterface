"""
Setup Panel for robot configuration and initialization.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QFormLayout,
    QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt


class SetupPanel(QWidget):
    """Panel for robot setup and configuration."""
    
    def __init__(self, robot_controller):
        """
        Initialize the setup panel.
        
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
        
        # Connection Group
        connection_group = QGroupBox("ROS 2 Connection")
        connection_layout = QFormLayout()
        
        self.namespace_edit = QLineEdit()
        self.namespace_edit.setPlaceholderText("/robot")
        connection_layout.addRow("Namespace:", self.namespace_edit)
        
        self.controller_edit = QLineEdit()
        self.controller_edit.setText("joint_trajectory_controller")
        connection_layout.addRow("Controller:", self.controller_edit)
        
        self.reconnect_btn = QPushButton("Reconnect")
        connection_layout.addRow("", self.reconnect_btn)
        
        connection_group.setLayout(connection_layout)
        layout.addWidget(connection_group)
        
        # Robot Configuration Group
        config_group = QGroupBox("Robot Configuration")
        config_layout = QFormLayout()
        
        self.robot_type_combo = QComboBox()
        self.robot_type_combo.addItems([
            "Generic 6-DOF",
            "Generic 7-DOF",
            "UR5",
            "UR10",
            "Panda",
            "Custom"
        ])
        config_layout.addRow("Robot Type:", self.robot_type_combo)
        
        self.dof_spin = QSpinBox()
        self.dof_spin.setRange(1, 10)
        self.dof_spin.setValue(6)
        config_layout.addRow("Degrees of Freedom:", self.dof_spin)
        
        self.apply_config_btn = QPushButton("Apply Configuration")
        config_layout.addRow("", self.apply_config_btn)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # MoveIt 2 Configuration
        moveit_group = QGroupBox("MoveIt 2 Configuration")
        moveit_layout = QFormLayout()
        
        self.planning_group_edit = QLineEdit()
        self.planning_group_edit.setText("manipulator")
        moveit_layout.addRow("Planning Group:", self.planning_group_edit)
        
        self.planner_combo = QComboBox()
        self.planner_combo.addItems([
            "RRTConnect",
            "RRT",
            "PRM",
            "TRRT",
            "EST"
        ])
        moveit_layout.addRow("Planner:", self.planner_combo)
        
        self.planning_time_spin = QDoubleSpinBox()
        self.planning_time_spin.setRange(0.1, 30.0)
        self.planning_time_spin.setValue(5.0)
        self.planning_time_spin.setSuffix(" s")
        moveit_layout.addRow("Planning Time:", self.planning_time_spin)
        
        self.enable_moveit_check = QCheckBox("Enable MoveIt 2")
        self.enable_moveit_check.setChecked(True)
        moveit_layout.addRow("", self.enable_moveit_check)
        
        moveit_group.setLayout(moveit_layout)
        layout.addWidget(moveit_group)
        
        # Joint Limits Group
        limits_group = QGroupBox("Joint Limits")
        limits_layout = QVBoxLayout()
        
        limits_layout.addWidget(QLabel("Configure joint velocity and acceleration limits:"))
        
        self.velocity_limit_spin = QDoubleSpinBox()
        self.velocity_limit_spin.setRange(0.1, 10.0)
        self.velocity_limit_spin.setValue(1.0)
        self.velocity_limit_spin.setSuffix(" rad/s")
        
        vel_layout = QHBoxLayout()
        vel_layout.addWidget(QLabel("Max Velocity:"))
        vel_layout.addWidget(self.velocity_limit_spin)
        limits_layout.addLayout(vel_layout)
        
        self.accel_limit_spin = QDoubleSpinBox()
        self.accel_limit_spin.setRange(0.1, 10.0)
        self.accel_limit_spin.setValue(2.0)
        self.accel_limit_spin.setSuffix(" rad/s²")
        
        accel_layout = QHBoxLayout()
        accel_layout.addWidget(QLabel("Max Acceleration:"))
        accel_layout.addWidget(self.accel_limit_spin)
        limits_layout.addLayout(accel_layout)
        
        limits_group.setLayout(limits_layout)
        layout.addWidget(limits_group)
        
        # System Information
        info_group = QGroupBox("System Information")
        info_layout = QVBoxLayout()
        
        self.system_info_text = QTextEdit()
        self.system_info_text.setReadOnly(True)
        self.system_info_text.setMaximumHeight(150)
        self.update_system_info()
        info_layout.addWidget(self.system_info_text)
        
        self.refresh_info_btn = QPushButton("Refresh Information")
        info_layout.addWidget(self.refresh_info_btn)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
    
    def connect_signals(self):
        """Connect signals and slots."""
        self.reconnect_btn.clicked.connect(self.reconnect_robot)
        self.apply_config_btn.clicked.connect(self.apply_configuration)
        self.refresh_info_btn.clicked.connect(self.update_system_info)
    
    def reconnect_robot(self):
        """Reconnect to robot."""
        QMessageBox.information(self, "Reconnect", 
                              "Reconnection functionality coming soon...")
    
    def apply_configuration(self):
        """Apply robot configuration."""
        robot_type = self.robot_type_combo.currentText()
        dof = self.dof_spin.value()
        
        QMessageBox.information(self, "Apply Configuration",
                              f"Configuration applied:\n"
                              f"Robot Type: {robot_type}\n"
                              f"DOF: {dof}")
    
    def update_system_info(self):
        """Update system information display."""
        info = "System Information:\n"
        info += "=" * 40 + "\n"
        
        if self.robot_controller.is_connected():
            info += "Status: Connected\n"
            joint_names = self.robot_controller.get_joint_names()
            info += f"Detected Joints: {len(joint_names)}\n"
            if joint_names:
                info += f"Joint Names: {', '.join(joint_names)}\n"
        else:
            info += "Status: Disconnected\n"
            info += "Waiting for robot connection...\n"
        
        info += f"\nROS 2 Node: {self.robot_controller.get_name()}\n"
        info += f"Namespace: {self.namespace_edit.text() or 'default'}\n"
        info += f"Controller: {self.controller_edit.text()}\n"
        
        self.system_info_text.setPlainText(info)
