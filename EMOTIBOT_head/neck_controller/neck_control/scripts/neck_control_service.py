#!/usr/bin/env python

import rospy
from dynamixel_workbench_msgs.srv import DynamixelCommand, DynamixelCommandRequest
from std_msgs.msg import Int32
import subprocess


def convert_to_value(degree):
    """
    Converts a degree value to a value in the range of 0-4096.
    """
    degree_range = 360.0 # 0~360도 범위 내에서 제어하고 있다고 가정
    value_range = 4096   # 0~4096 범위 내의 출력값
    # 범위를 0~1 사이의 값으로 정규화하고 value_range를 곱해서 출력값으로 변환
    value = int((degree / degree_range) * value_range)
    return value

def dynamixel_controller_callback(data):
    try:
        # 서비스 클라이언트 생성
        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
        dynamixel_command_client = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)

        # 요청 메시지 생성
        command = 'goal_position'
        id = 1
        addr_name = 'Goal_Position'

        value = convert_to_value(data.data)

        request = DynamixelCommandRequest()
        request.command = command
        request.id = id
        request.addr_name = addr_name
        request.value = value

        # 서비스 요청
        response = dynamixel_command_client(request)

        rospy.loginfo(response)

    except rospy.ServiceException as e:
        rospy.logerr("Service call failed: %s"%e)



if __name__ == '__main__':

    rospy.init_node('neck_controller')
    rospy.Subscriber('EMOTIBOT/neck_position', Int32, dynamixel_controller_callback)
    rospy.spin()
