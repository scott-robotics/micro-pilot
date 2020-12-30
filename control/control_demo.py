#!/usr/bin/env python3

import rospy
import servo

from sensor_msgs.msg import Joy

rospy.init_node('servo_control')

controller = servo.ServoController('/dev/ttyACM0')

def joystick_callback(msg):
    controller.set_target_norm(0, msg.axes[3])
    controller.set_target_norm(1, msg.axes[1])

def display_position(event):
    print('Steering:', controller.get_position(0))
    print('Throttle:', controller.get_position(1))


rospy.Subscriber('/joy', Joy, joystick_callback)
rospy.Timer(rospy.Duration(0.25), display_position)

rospy.spin()
