from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'open_robotics_interface'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='OpenRobotics Team',
    maintainer_email='dev@example.com',
    description='A graphical interface for controlling robots with ROS 2 and MoveIt 2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_gui = open_robotics_interface.main:main',
        ],
    },
)
