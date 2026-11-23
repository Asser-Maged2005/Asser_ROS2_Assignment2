# Asser_ROS2_Assignment2
ROS2 assignment 2 by Asser Maged, Osama Mohamed & Youssef Mahmoud

1- Build the workspace:
```bash
cd ~/ROS_assign2
colcon build
source install/setup.bash
```

2- Upload the microcontroller firmware:
Open `firmware/servo_receiver.ino` in Arduino IDE and flash it to your ESP32 or Arduino Uno (`115200` baud).

3- Wire the servos (power servos from an external $5\text{V–}6\text{V}$ supply and tie all GNDs together):
- `joint1` (Base yaw): **GPIO 13** (ESP32) / **D3** (Arduino Uno)
- `joint2` (Shoulder pitch): **GPIO 12** (ESP32) / **D5** (Arduino Uno)
- `joint3` (Elbow pitch): **GPIO 14** (ESP32) / **D6** (Arduino Uno)
- `joint4` (Wrist pitch): **GPIO 27** (ESP32) / **D9** (Arduino Uno)
- `GND`: External $5\text{V}$ PSU `GND` + Servo `GND` + Microcontroller `GND`

4- Connect the microcontroller over USB and allow serial port access:
```bash
sudo chmod a+rw /dev/ttyUSB0
```
*(Use `/dev/ttyACM0` if using an Arduino Uno.)*

5- Launch Gazebo, RViz2, the Serial Bridge, and the Sliders GUI together:
```bash
ros2 launch arm_description full_system.launch.py port:=/dev/ttyUSB0
```
*(Use `port:=/dev/ttyACM0` for Arduino Uno.)* Drag any slider in the **4-DOF Arm Trajectory Controller** window to move Gazebo, RViz2, and your physical servos at the same time.

---

### Optional: Run Components Separately
- **Simulation only (Gazebo + RViz2):** `ros2 launch arm_description sim.launch.py`
- **Sliders GUI only:** `ros2 run arm_control arm_gui`
- **Automated pose loop:** `ros2 run arm_control trajectory_publisher`
- **Serial bridge only:** `ros2 run arm_control serial_bridge --ros-args -p port:=/dev/ttyUSB0`

### Reference
- **Packages:** `arm_description` (4-DOF URDF, Gazebo world, RViz2 config, launch files) & `arm_control` (`arm_gui`, `serial_bridge`, `trajectory_publisher`).
- **Dependencies:** ROS 2 Lyrical (`robot_state_publisher`, `rviz2`, `ros_gz_sim`, `ros_gz_bridge`), `python3-serial`, `python3-tk`.
- **Serial Protocol:** USB Serial (`115200` baud) sending ASCII CSV `<j1>,<j2>,<j3>,<j4>\n` with joint radians $[-\frac{\pi}{2}, +\frac{\pi}{2}]$ mapped to $[0, 180]^\circ$.
