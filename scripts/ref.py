#!/usr/bin/env python3


import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray

import sys, select, termios, tty

msg = """
Control Your Toy!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly
CTRL-C to quit
"""

moveBindings = {
        'i':(1,0),
        'o':(1,-1),
        'j':(0,1),
        'l':(0,-1),
        'u':(1,1),
        ',':(-1,0),
        '.':(-1,1),
        'm':(-1,-1),
           }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
          }

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

speed = 8
turn = 0.5

def vels(speed,turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    
    rospy.init_node('turtlebot_teleop')

    pub_right = rospy.Publisher('/toy_car2/joint1_position_controller/command', Float64, queue_size=10) # Add your topic here between ''. Eg '/my_robot/steering_controller/command'
    pub_left = rospy.Publisher('/toy_car2/joint2_position_controller/command', Float64, queue_size=10)
    pub_move1 = rospy.Publisher('/toy_car2/joint3_position_controller/command', Float64, queue_size=10) # Add your topic for move here '' Eg '/my_robot/longitudinal_controller/command'
    pub_move2 = rospy.Publisher('/toy_car2/joint4_position_controller/command', Float64, queue_size=10)

    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    try:
        print (msg)
        print (vels(speed,turn))
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0

                print (vels(speed,turn))
                if (status == 14):
                    print (msg)
                status = (status + 1) % 15
            elif key == ' ' or key == 'k' :
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break

            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            pub_right.publish(control_turn) # publish the turn command.
            pub_left.publish(control_turn) # publish the turn command.
            pub_move1.publish(50*control_speed) # publish the control speed. 
            pub_move2.publish(50*control_speed)

    except:
        print (e)

    finally:
        pub_right.publish(control_turn)
        pub_left.publish(control_turn)
        pub_move1.publish(control_speed)
        pub_move2.publish(control_speed)
        # twist = Twist()
        # twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        # twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        # pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)



class Robot(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.joint_trajectory_pub = self.create_publisher(Float64MultiArray, '/joint_position_controller/commands', 10)
        self.joint_positions_pub = self.create_publisher(Float64MultiArray, '/velocity_controller/commands', 10)
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.begin_time=self.get_clock().now()

    def publish_data(self):
        

        # Publish Float64MultiArray message
        # joint_positions = Float64MultiArray()
        # joint_positions.data = [100.0, 100.0, 100.0, 100.0]  # Replace with your joint positions
        # self.joint_positions_pub.publish(joint_positions)

        joint_positions = Float64MultiArray()
        joint_positions.data = [1.5, 1.5, 1.5, 1.5]  # Replace with your joint positions
        self.joint_trajectory_pub.publish(joint_positions)

        # # Publish JointState message
        # joint_state = JointState()
        # joint_state.header.stamp = self.get_clock().now().to_msg()
        # joint_state.name = joint_trajectory.joint_names
        # joint_state.position = joint_positions.data
        # joint_state.velocity = point.velocities
        # self.joint_state_pub.publish(joint_state)


def main(args=None):
    rclpy.init(args=args)
    joint_control_publisher = Robot()
    rclpy.spin(joint_control_publisher)
    joint_control_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
