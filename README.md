## Project Description
This repository contains the first laboratory work on robotics. The goal is to design and simulate a mobile robot using the **SDF (Simulation Description Format)** within the **Gazebo Harmonic** environment. The project is fully containerized using **Docker** to ensure environment consistency across different systems.



## Prerequisites
To run this project, you need:
* **Windows 11** with **WSL2** (Ubuntu 24.04)
* **Docker Desktop** (WSL2 backend enabled)
* **WSLg** or an X-server (like VcXsrv) for GUI rendering

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/gipain/robotics_lab1.git
cd robotics_lab1
```
### 2. Build Docker Image

```bash
./scripts/cmd build-docker
```

This takes 10-15 minutes on first run.

### 3. Run Container

```bash
./scripts/cmd run
```
### 4. Install and open VScode

```bash
code .
```


#### Open Additional Terminals for testing

```bash
# In a new terminal window
./scripts/cmd bash
```
---
## Testing
### Launching
To test simulation you need to launch gazebo simulation
```bash
gz sim /opt/ws/src/code/lab1/worlds/robot.sdf
```
### Controling
To control your robot you can use Teleop plugin to control using WASD. But you can also control robot by sending messages to topic "/cmd_vel" inside your second terminal.
For example:
```bash
gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.0}"
```
### Verify LiDAR sensor data
To verify that the LiDAR is scanning the obstacles, open a third terminal, enter the container (./scripts/cmd bash), and read the live data stream:
```bash
gz topic -e -t /lidar
```
Press Ctrl+C to stop the data stream.
