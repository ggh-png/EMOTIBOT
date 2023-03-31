#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32
from dynamixel_sdk import *

# Control table address
ADDR_PRO_GOAL_POSITION = 116  # EEPROM Address for Goal Position

class neck_controller:
    def __init__(self):
        rospy.init_node('neck_controller')

        # Set parameters from the ROS parameter server or default values
        self.dxl_id = rospy.get_param('~dxl_id', 1)
        self.port = rospy.get_param('~port', '/dev/ttyUSB1')
        self.baudrate = rospy.get_param('~baudrate', 57600)

        # Initialize PortHandler instance
        self.port_handler = PortHandler(self.port)

        # Initialize PacketHandler instance
        self.packet_handler = PacketHandler(2.0)

        # Open port
        if self.port_handler.openPort():
            rospy.loginfo("Succeeded to open the port %s" % self.port)
        else:
            rospy.logerr("Failed to open the port %s" % self.port)

        # Set baudrate
        if self.port_handler.setBaudRate(self.baudrate):
            rospy.loginfo("Succeeded to change the baudrate %d" % self.baudrate)
        else:
            rospy.logerr("Failed to change the baudrate %d" % self.baudrate)

        # Enable torque
        self.set_torque_enable(True)

        # Subscribe to the topic
        rospy.Subscriber('EMOTIROBOT/neck_position', Int32, self.dynamixel_position_callback)

        # Set loop rate
        self.rate = rospy.Rate(10) # 10Hz

    def set_torque_enable(self, enable):
        dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(self.port_handler, self.dxl_id, 64, int(enable))
        if dxl_comm_result != COMM_SUCCESS:
            rospy.logerr("Failed to enable torque")
        elif dxl_error != 0:
            rospy.logerr("Received error packet")

    def set_goal_position(self, goal_position):
        # Write goal position
        dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, self.dxl_id, ADDR_PRO_GOAL_POSITION, goal_position)
        if dxl_comm_result != COMM_SUCCESS:
            rospy.logerr("Failed to write goal position")
        elif dxl_error != 0:
            rospy.logerr("Received error packet")

    def dynamixel_position_callback(self, msg):
        goal_position = msg.data
        self.set_goal_position(goal_position)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()

if __name__ == '__main__':
    try:
        controller = neck_controller()
        controller.run()
    except rospy.ROSInterruptException:
        pass
