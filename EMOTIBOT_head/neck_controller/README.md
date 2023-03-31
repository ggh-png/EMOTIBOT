# neck_control

![rosgraph](https://user-images.githubusercontent.com/71277820/225289793-63cf4dfb-b062-49fe-9bbe-9cfc3af3b052.png)

## install



```bash
cd
cd catkin_ws/src
git clone https://github.com/ggh-png/neck_controller.git
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
cd ~/catkin_ws && catkin_make
```

### 우분투 환경에서 다이나믹셀 정보 찾기


```bash
rosrun dynamixel_workbench_controllers find_dynamixel /dev/ttyUSB0
```

### neck control launch


```bash
roslaunch neck_control neck_control.launch 
```

### ros topic position control

> min & max : 0 ~ 4096
> 


```bash
rostopic pub /EMOTIROBOT/neck_position std_msgs/Int32 "data: 100"
```
