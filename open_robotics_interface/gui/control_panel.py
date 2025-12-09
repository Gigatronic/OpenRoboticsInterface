"""
Control Panel for manual robot control and jogging.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QPushButton, QSlider, QLabel, QComboBox, QSpinBox,
    QDoubleSpinBox, QGridLayout
)
from PyQt5.QtCore import Qt
import math


class ControlPanel(QWidget):
    """Panel for manual robot control operations."""
    
    def __init__(self, robot_controller):
        """
        Initialize the control panel.
        
        Args:
            robot_controller: RobotController instance
        """
        super().__init__()
        
        self.robot_controller = robot_controller
        self.current_joint_positions = {}
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Joint Control Group
        joint_group = QGroupBox("Joint Control")
        joint_layout = QVBoxLayout()
        
        # Joint selection
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Select Joint:"))
        self.joint_combo = QComboBox()
        selection_layout.addWidget(self.joint_combo)
        joint_layout.addLayout(selection_layout)
        
        # Jog controls
        jog_layout = QHBoxLayout()
        self.jog_minus_btn = QPushButton("◄ Jog -")
        self.jog_plus_btn = QPushButton("Jog + ►")
        jog_layout.addWidget(self.jog_minus_btn)
        jog_layout.addWidget(self.jog_plus_btn)
        joint_layout.addLayout(jog_layout)
        
        # Jog step size
        step_layout = QHBoxLayout()
        step_layout.addWidget(QLabel("Jog Step (deg):"))
        self.jog_step_spin = QDoubleSpinBox()
        self.jog_step_spin.setRange(0.1, 45.0)
        self.jog_step_spin.setValue(5.0)
        self.jog_step_spin.setSuffix("°")
        step_layout.addWidget(self.jog_step_spin)
        joint_layout.addLayout(step_layout)
        
        joint_group.setLayout(joint_layout)
        layout.addWidget(joint_group)
        
        # Joint Positions Group
        positions_group = QGroupBox("Current Joint Positions")
        self.positions_layout = QVBoxLayout()
        self.joint_labels = {}
        positions_group.setLayout(self.positions_layout)
        layout.addWidget(positions_group)
        
        # Quick Actions Group
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QGridLayout()
        
        self.home_btn = QPushButton("Home Position")
        self.home_btn.setMinimumHeight(50)
        actions_layout.addWidget(self.home_btn, 0, 0)
        
        self.stop_btn = QPushButton("Stop Motion")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setStyleSheet("background-color: #ff4444; color: white;")
        actions_layout.addWidget(self.stop_btn, 0, 1)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Cartesian Control Group
        cartesian_group = QGroupBox("Cartesian Control")
        cartesian_layout = QVBoxLayout()
        cartesian_layout.addWidget(QLabel("Cartesian jogging coming soon..."))
        cartesian_group.setLayout(cartesian_layout)
        layout.addWidget(cartesian_group)
        
        layout.addStretch()
    
    def connect_signals(self):
        """Connect signals and slots."""
        self.robot_controller.joint_state_updated.connect(self.update_joint_display)
        self.jog_minus_btn.clicked.connect(self.jog_minus)
        self.jog_plus_btn.clicked.connect(self.jog_plus)
        self.home_btn.clicked.connect(self.robot_controller.home_robot)
        self.stop_btn.clicked.connect(lambda: self.robot_controller.publish_status("STOP"))
    
    def update_joint_display(self, joint_states):
        """Update the joint position display."""
        self.current_joint_positions = joint_states
        
        # Update combo box if needed
        if self.joint_combo.count() == 0:
            for joint_name in sorted(joint_states.keys()):
                self.joint_combo.addItem(joint_name)
        
        # Update position labels
        for joint_name, state in joint_states.items():
            if joint_name not in self.joint_labels:
                label = QLabel()
                self.joint_labels[joint_name] = label
                self.positions_layout.addWidget(label)
            
            position_deg = math.degrees(state['position'])
            self.joint_labels[joint_name].setText(
                f"{joint_name}: {position_deg:.2f}° ({state['position']:.3f} rad)"
            )
    
    def jog_minus(self):
        """Jog selected joint in negative direction."""
        joint_name = self.joint_combo.currentText()
        if joint_name:
            step_rad = math.radians(-self.jog_step_spin.value())
            self.robot_controller.jog_joint(joint_name, step_rad)
    
    def jog_plus(self):
        """Jog selected joint in positive direction."""
        joint_name = self.joint_combo.currentText()
        if joint_name:
            step_rad = math.radians(self.jog_step_spin.value())
            self.robot_controller.jog_joint(joint_name, step_rad)
