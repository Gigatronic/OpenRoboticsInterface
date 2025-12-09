#!/usr/bin/env python3
"""Test that all modules can be imported."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_core_imports():
    """Test core module imports."""
    try:
        import open_robotics_interface
        print("✓ open_robotics_interface imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import open_robotics_interface: {e}")
        return False
    
    try:
        from open_robotics_interface import gui
        print("✓ gui module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import gui module: {e}")
        return False
    
    try:
        from open_robotics_interface import ros2_interface
        print("✓ ros2_interface module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ros2_interface module: {e}")
        return False
    
    try:
        from open_robotics_interface import utils
        print("✓ utils module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils module: {e}")
        return False
    
    return True

def test_gui_imports():
    """Test GUI module imports (may fail if PyQt5 not installed)."""
    try:
        from open_robotics_interface.gui import control_panel
        print("✓ control_panel imported successfully")
    except ImportError as e:
        print(f"⚠ Failed to import control_panel (PyQt5 may not be installed): {e}")
        return False
    
    try:
        from open_robotics_interface.gui import programming_panel
        print("✓ programming_panel imported successfully")
    except ImportError as e:
        print(f"⚠ Failed to import programming_panel: {e}")
        return False
    
    try:
        from open_robotics_interface.gui import setup_panel
        print("✓ setup_panel imported successfully")
    except ImportError as e:
        print(f"⚠ Failed to import setup_panel: {e}")
        return False
    
    try:
        from open_robotics_interface.gui import visualization_panel
        print("✓ visualization_panel imported successfully")
    except ImportError as e:
        print(f"⚠ Failed to import visualization_panel: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("Testing OpenRoboticsInterface imports...\n")
    
    success = True
    success = test_core_imports() and success
    print()
    
    gui_success = test_gui_imports()
    if not gui_success:
        print("\nNote: GUI import failures are expected if PyQt5 is not installed.")
        print("Install with: pip install PyQt5 pyqtgraph")
    
    print("\n" + "=" * 50)
    if success:
        print("Core imports: PASSED")
    else:
        print("Core imports: FAILED")
        sys.exit(1)
