
![camera_control](https://user-images.githubusercontent.com/71277820/226186643-13d10d46-7f89-4a32-b8b2-aff7c31f51ca.png)

## install

---

```bash
git clone https://github.com/ggh-png/EMOTIROBOT.git
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
cd ~/catkin_ws && catkin_make
```

### neck_control_service launch

---

```bash
roslaunch neck_control neck_control_service.launch
```

### camera_tracking launch

---

```bash
rosrun camera_tracking camera_tracking_node.py
```