"""
Main Window for OpenRoboticsInterface.
Provides the primary user interface for robot control and programming.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QStatusBar, QMenuBar, QMenu, QAction,
    QMessageBox, QLabel
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

from open_robotics_interface.gui.control_panel import ControlPanel
from open_robotics_interface.gui.programming_panel import ProgrammingPanel
from open_robotics_interface.gui.setup_panel import SetupPanel
from open_robotics_interface.gui.visualization_panel import VisualizationPanel


class MainWindow(QMainWindow):
    """Main application window for the OpenRoboticsInterface."""
    
    def __init__(self, robot_controller):
        """
        Initialize the main window.
        
        Args:
            robot_controller: RobotController instance for ROS 2 communication
        """
        super().__init__()
        
        self.robot_controller = robot_controller
        
        # Set up the UI
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Set up update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(100)  # Update every 100ms
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle('OpenRoboticsInterface - Robot Control')
        self.setGeometry(100, 100, 1400, 900)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget with tab structure
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create panels
        self.control_panel = ControlPanel(self.robot_controller)
        self.programming_panel = ProgrammingPanel(self.robot_controller)
        self.setup_panel = SetupPanel(self.robot_controller)
        self.visualization_panel = VisualizationPanel(self.robot_controller)
        
        # Add tabs
        self.tab_widget.addTab(self.control_panel, "Control")
        self.tab_widget.addTab(self.programming_panel, "Programming")
        self.tab_widget.addTab(self.setup_panel, "Setup")
        self.tab_widget.addTab(self.visualization_panel, "Visualization")
        
        main_layout.addWidget(self.tab_widget)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.connection_status_label = QLabel("Disconnected")
        self.status_bar.addPermanentWidget(self.connection_status_label)
        
        self.status_bar.showMessage('Ready')
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        load_config_action = QAction('&Load Configuration', self)
        load_config_action.triggered.connect(self.load_configuration)
        file_menu.addAction(load_config_action)
        
        save_config_action = QAction('&Save Configuration', self)
        save_config_action.triggered.connect(self.save_configuration)
        file_menu.addAction(save_config_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Robot menu
        robot_menu = menubar.addMenu('&Robot')
        
        home_action = QAction('&Home Robot', self)
        home_action.triggered.connect(self.home_robot)
        robot_menu.addAction(home_action)
        
        stop_action = QAction('&Emergency Stop', self)
        stop_action.setShortcut('Space')
        stop_action.triggered.connect(self.emergency_stop)
        robot_menu.addAction(stop_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def connect_signals(self):
        """Connect signals from robot controller to UI."""
        self.robot_controller.robot_status_updated.connect(self.on_status_update)
    
    def on_status_update(self, status_msg):
        """Handle status updates from robot controller."""
        self.status_bar.showMessage(status_msg)
    
    def update_status(self):
        """Update connection status indicator."""
        if self.robot_controller.is_connected():
            self.connection_status_label.setText("Connected")
            self.connection_status_label.setStyleSheet("color: green")
        else:
            self.connection_status_label.setText("Disconnected")
            self.connection_status_label.setStyleSheet("color: red")
    
    def load_configuration(self):
        """Load robot configuration from file."""
        # TODO: Implement configuration loading
        QMessageBox.information(self, 'Load Configuration', 
                              'Configuration loading not yet implemented')
    
    def save_configuration(self):
        """Save robot configuration to file."""
        # TODO: Implement configuration saving
        QMessageBox.information(self, 'Save Configuration', 
                              'Configuration saving not yet implemented')
    
    def home_robot(self):
        """Send robot to home position."""
        reply = QMessageBox.question(self, 'Home Robot',
                                    'Move robot to home position?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.robot_controller.home_robot()
            self.status_bar.showMessage('Moving to home position...')
    
    def emergency_stop(self):
        """Trigger emergency stop."""
        self.robot_controller.publish_status('EMERGENCY STOP')
        self.status_bar.showMessage('EMERGENCY STOP TRIGGERED', 5000)
        QMessageBox.warning(self, 'Emergency Stop', 
                          'Emergency stop triggered. Please restart the robot controller.')
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(self, 'About OpenRoboticsInterface',
                         '<h2>OpenRoboticsInterface v0.1.0</h2>'
                         '<p>A graphical interface for controlling robots with ROS 2 and MoveIt 2.</p>'
                         '<p>This application provides intuitive control, programming, and '
                         'setup capabilities for robotic systems.</p>'
                         '<p>© 2025 OpenRobotics Team</p>')
    
    def closeEvent(self, event):
        """Handle window close event."""
        reply = QMessageBox.question(self, 'Exit',
                                    'Are you sure you want to exit?',
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
