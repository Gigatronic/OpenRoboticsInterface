"""
Programming Panel for creating and executing robot programs.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QTextEdit, QListWidget, QLabel,
    QInputDialog, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt


class ProgrammingPanel(QWidget):
    """Panel for robot programming and trajectory creation."""
    
    def __init__(self, robot_controller):
        """
        Initialize the programming panel.
        
        Args:
            robot_controller: RobotController instance
        """
        super().__init__()
        
        self.robot_controller = robot_controller
        self.program_points = []
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        
        # Create splitter for side-by-side layout
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Program list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_layout.addWidget(QLabel("Program Points:"))
        self.points_list = QListWidget()
        left_layout.addWidget(self.points_list)
        
        # Point control buttons
        point_buttons_layout = QHBoxLayout()
        self.add_point_btn = QPushButton("Add Current Position")
        self.remove_point_btn = QPushButton("Remove Selected")
        self.clear_all_btn = QPushButton("Clear All")
        point_buttons_layout.addWidget(self.add_point_btn)
        point_buttons_layout.addWidget(self.remove_point_btn)
        point_buttons_layout.addWidget(self.clear_all_btn)
        left_layout.addLayout(point_buttons_layout)
        
        splitter.addWidget(left_widget)
        
        # Right side - Program execution
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Program info
        info_group = QGroupBox("Program Information")
        info_layout = QVBoxLayout()
        self.program_info_text = QTextEdit()
        self.program_info_text.setMaximumHeight(100)
        self.program_info_text.setReadOnly(True)
        self.program_info_text.setPlainText("No program loaded")
        info_layout.addWidget(self.program_info_text)
        info_group.setLayout(info_layout)
        right_layout.addWidget(info_group)
        
        # Execution controls
        exec_group = QGroupBox("Execution")
        exec_layout = QVBoxLayout()
        
        self.run_program_btn = QPushButton("Run Program")
        self.run_program_btn.setMinimumHeight(60)
        self.run_program_btn.setStyleSheet("background-color: #44ff44; font-size: 16px;")
        exec_layout.addWidget(self.run_program_btn)
        
        self.pause_btn = QPushButton("Pause")
        self.stop_program_btn = QPushButton("Stop")
        
        pause_stop_layout = QHBoxLayout()
        pause_stop_layout.addWidget(self.pause_btn)
        pause_stop_layout.addWidget(self.stop_program_btn)
        exec_layout.addLayout(pause_stop_layout)
        
        exec_group.setLayout(exec_layout)
        right_layout.addWidget(exec_group)
        
        # Program management
        manage_group = QGroupBox("Program Management")
        manage_layout = QVBoxLayout()
        
        self.save_program_btn = QPushButton("Save Program")
        self.load_program_btn = QPushButton("Load Program")
        manage_layout.addWidget(self.save_program_btn)
        manage_layout.addWidget(self.load_program_btn)
        
        manage_group.setLayout(manage_layout)
        right_layout.addWidget(manage_group)
        
        right_layout.addStretch()
        
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
    
    def connect_signals(self):
        """Connect signals and slots."""
        self.add_point_btn.clicked.connect(self.add_current_position)
        self.remove_point_btn.clicked.connect(self.remove_selected_point)
        self.clear_all_btn.clicked.connect(self.clear_all_points)
        self.run_program_btn.clicked.connect(self.run_program)
        self.pause_btn.clicked.connect(self.pause_program)
        self.stop_program_btn.clicked.connect(self.stop_program)
        self.save_program_btn.clicked.connect(self.save_program)
        self.load_program_btn.clicked.connect(self.load_program)
    
    def add_current_position(self):
        """Add current robot position as a program point."""
        positions = self.robot_controller.get_current_joint_positions()
        
        if not positions:
            QMessageBox.warning(self, "No Position", 
                              "Cannot add point: No robot position available")
            return
        
        # Get point name from user
        name, ok = QInputDialog.getText(self, "Point Name", 
                                        "Enter name for this point:",
                                        text=f"Point_{len(self.program_points) + 1}")
        
        if ok and name:
            self.program_points.append({
                'name': name,
                'positions': positions.copy()
            })
            self.points_list.addItem(name)
            self.update_program_info()
    
    def remove_selected_point(self):
        """Remove the selected program point."""
        current_row = self.points_list.currentRow()
        if current_row >= 0:
            self.points_list.takeItem(current_row)
            del self.program_points[current_row]
            self.update_program_info()
    
    def clear_all_points(self):
        """Clear all program points."""
        reply = QMessageBox.question(self, "Clear All",
                                    "Clear all program points?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.points_list.clear()
            self.program_points.clear()
            self.update_program_info()
    
    def update_program_info(self):
        """Update program information display."""
        if not self.program_points:
            self.program_info_text.setPlainText("No program loaded")
        else:
            info = f"Program with {len(self.program_points)} points:\n"
            for i, point in enumerate(self.program_points, 1):
                info += f"{i}. {point['name']}\n"
            self.program_info_text.setPlainText(info)
    
    def run_program(self):
        """Execute the programmed trajectory."""
        if not self.program_points:
            QMessageBox.warning(self, "No Program", 
                              "No program points to execute")
            return
        
        QMessageBox.information(self, "Run Program",
                              f"Executing program with {len(self.program_points)} points...")
        
        # Execute each point in sequence
        for point in self.program_points:
            self.robot_controller.move_joints(point['positions'], duration=2.0)
            # In a real implementation, we would wait for completion
    
    def pause_program(self):
        """Pause program execution."""
        QMessageBox.information(self, "Pause", "Program paused")
    
    def stop_program(self):
        """Stop program execution."""
        self.robot_controller.publish_status("Program stopped")
        QMessageBox.information(self, "Stop", "Program stopped")
    
    def save_program(self):
        """Save program to file."""
        if not self.program_points:
            QMessageBox.warning(self, "No Program", "No program to save")
            return
        
        QMessageBox.information(self, "Save Program", 
                              "Program save functionality coming soon...")
    
    def load_program(self):
        """Load program from file."""
        QMessageBox.information(self, "Load Program", 
                              "Program load functionality coming soon...")
