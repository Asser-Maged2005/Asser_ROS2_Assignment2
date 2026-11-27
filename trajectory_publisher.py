import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class ArmTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('arm_trajectory_publisher')
        self.publisher_ = self.create_publisher(
            JointTrajectory, '/arm_controller/joint_trajectory', 10
        )
        self.timer = self.create_timer(3.0, self.publish_pose)
        self.step = 0
        self.poses = [
            [0.0, 0.0, 0.0, 0.0],
            [0.6, 0.5, -0.7, 0.4],
            [-0.6, 0.7, -0.9, 0.3],
            [0.0, 0.3, -0.4, 0.2],
        ]

    def publish_pose(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']
        point = JointTrajectoryPoint()
        point.positions = self.poses[self.step % len(self.poses)]
        point.time_from_start = Duration(sec=2, nanosec=0)
        msg.points = [point]
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published trajectory: {point.positions}')
        self.step += 1


def main(args=None):
    rclpy.init(args=args)
    node = ArmTrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
