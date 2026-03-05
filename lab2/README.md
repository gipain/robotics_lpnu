ROS 2 Jazzy - Lab 2: Robotics Simulation
Project Description
This repository contains the source code for Lab 2 of the Robotics course at LPNU. The project involves creating a ROS 2 package for robot simulation using Gazebo and visualization in RViz2. It is built using the ament_python build type.

System Requirements
Operating System: Ubuntu 24.04 LTS (Noble Numbat) running on WSL2.

ROS 2 Version: Jazzy Jalisco.

Simulation Tools: Gazebo Sim and RViz2.

Installation & Setup
1. Environment Preparation
If you encounter network resolution issues in WSL2, reset the DNS settings:

Bash
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
DNS Fix: Resolves "Temporary failure resolving" errors during apt update.

2. ROS 2 and Dependencies
Install the core ROS 2 Desktop and the necessary Gazebo integration packages:

Bash
sudo apt update
sudo apt install ros-jazzy-desktop
sudo apt install ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge
ros_gz_sim: Provides the Gazebo simulation environment.

ros_gz_bridge: Bridges communication between ROS 2 topics and Gazebo.

3. VS Code Configuration
To resolve Python import errors like Import "launch" could not be resolved, update your .vscode/settings.json:

JSON
{
    "python.analysis.extraPaths": [
        "/opt/ros/jazzy/lib/python3.12/site-packages"
    ]
}
Interpreter: Ensure the Python interpreter is set to /usr/bin/python3 (WSL: Ubuntu).

Workspace Setup
Create the workspace and clone the package:

Bash
mkdir -p ~/robotics_lpnu/src
cd ~/robotics_lpnu/src
# (Place your lab2 folder here)
Build the package:

Bash
cd ~/robotics_lpnu
colcon build --packages-select lab2
colcon build: Generates the install folder required for execution.

Usage
To launch the simulation and visualization, run the following commands:

Source the environments:

Bash
source /opt/ros/jazzy/setup.bash
source ~/robotics_lpnu/install/setup.bash
Execute the launch file:

Bash
ros2 launch lab2 gazebo_ros2.launch.py
Launch File: Initializes Gazebo, spawns the robot model, and opens RViz2.

Troubleshooting
Package Not Found: Ensure you have run source install/setup.bash from the root of the robotics_lpnu workspace.

Yellow Squiggles in VS Code: Verify that the Python interpreter is pointing to the Linux path (/usr/bin/python3) and not a Windows path.