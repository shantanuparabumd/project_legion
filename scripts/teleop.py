#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Float64MultiArray
from rclpy.duration import Duration
from sensor_msgs.msg import JointState

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
        joint_positions.data = [1.0, 1.0, 1.0, 1.0]  # Replace with your joint positions
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
