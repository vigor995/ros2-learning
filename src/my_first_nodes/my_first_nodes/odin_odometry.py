import math

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped


class OdinOdometry(Node):
    """模拟 Odin1 同时输出位姿（Odometry）和轨迹（Path）"""

    def __init__(self):
        super().__init__('odin_odometry')

        self.odom_pub = self.create_publisher(Odometry, '/odin1/odom', 10)
        self.path_pub = self.create_publisher(Path, '/odin1/path', 10)

        self.t = 0.0
        self.path = Path()
        self.max_points = 700          # 只保留最近 700 个点（约一圈）

        self.create_timer(0.02, self.timer_callback)
        self.get_logger().info('Odin1 odometry + path publisher started')

    def get_pose(self):
        """算出当前时刻的位置和朝向（和 odin_pose_tf 一样的绕圈）"""
        theta = self.t * 0.5
        x = math.cos(theta) * 2.0
        y = math.sin(theta) * 2.0
        yaw = theta + math.pi / 2      # 朝运动方向
        return x, y, yaw

    def timer_callback(self):
        self.t += 0.02
        x, y, yaw = self.get_pose()
        stamp = self.get_clock().now().to_msg()

        # ===== 1. 里程计：位姿 + 速度 + 置信度 =====
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'map'          # 位姿是相对哪
        odom.child_frame_id = 'base_link'     # 机器人本体

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.z = math.sin(yaw / 2)
        odom.pose.pose.orientation.w = math.cos(yaw / 2)

        # 速度：绕圈的切线速度 = 半径 x 角速度 = 2.0 x 0.5 = 1.0 m/s
        odom.twist.twist.linear.x = 2.0 * 0.5
        odom.twist.twist.angular.z = 0.5

        # 协方差：对角线代表各分量的不确定度
        # 0.05 米的标准差 -> 方差 0.05 * 0.05 = 0.0025
        odom.pose.covariance[0] = 0.0025      # x 方向：±5cm
        odom.pose.covariance[7] = 0.0025      # y 方向：±5cm
        odom.pose.covariance[35] = 0.01       # 朝向

        self.odom_pub.publish(odom)

        # ===== 2. 轨迹：把每个位置累积成一条线 =====
        pose = PoseStamped()
        pose.header.stamp = stamp
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        pose.pose.orientation.z = math.sin(yaw / 2)
        pose.pose.orientation.w = math.cos(yaw / 2)

        self.path.header.stamp = stamp
        self.path.header.frame_id = 'map'
        self.path.poses.append(pose)
        if len(self.path.poses) > self.max_points:
            self.path.poses.pop(0)            # 丢掉最老的，防止无限增长
        self.path_pub.publish(self.path)


def main(args=None):
    rclpy.init(args=args)
    node = OdinOdometry()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
