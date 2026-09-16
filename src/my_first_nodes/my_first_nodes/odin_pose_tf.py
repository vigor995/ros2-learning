import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class OdinPoseTF(Node):
    """模拟 Odin1 的位姿输出：让 base_link 在 map 里绕圈走"""

    def __init__(self):
        super().__init__('odin_pose_tf')
        self.br = TransformBroadcaster(self)
        self.t = 0.0
        self.create_timer(0.02, self.timer_callback)
        self.get_logger().info('Odin1 pose TF broadcaster started')

    def timer_callback(self):
        self.t += 0.02

        ts = TransformStamped()
        ts.header.stamp = self.get_clock().now().to_msg()
        ts.header.frame_id = 'map'
        ts.child_frame_id = 'base_link'

        theta = self.t * 0.5
        ts.transform.translation.x = math.cos(theta) * 2.0
        ts.transform.translation.y = math.sin(theta) * 2.0
        ts.transform.translation.z = 0.0

        yaw = theta + math.pi / 2
        ts.transform.rotation.z = math.sin(yaw / 2)
        ts.transform.rotation.w = math.cos(yaw / 2)

        self.br.sendTransform(ts)


def main(args=None):
    rclpy.init(args=args)
    node = OdinPoseTF()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
