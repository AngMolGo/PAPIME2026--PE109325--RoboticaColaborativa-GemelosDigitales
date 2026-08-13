# Interfaces personalizadas

Por lo general, y es recomendable, las interfaces personalizadas se desarrollan en un paquete exclusivo para este fin.

# Universal Robots ROS2 Driver

Para ejecutar el driver:

``` bash
# Replace ur5e with one of ur3, ur3e, ur5, ur5e, ur7e, ur10, ur10e, ur12e, ur16e, ur8long, ur15, ur18, ur20, ur30
# Replace the IP address with the IP address of your actual robot / URSim
ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur5e robot_ip:=192.168.1.3 launch_rviz:=false
```
