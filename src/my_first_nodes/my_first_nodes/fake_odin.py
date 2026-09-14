"""
fake_odin.py —— 模拟 Odin1 发布点云

【为什么做这个】
Odin1 最核心的输出就是点云（每秒最多 70 万个点）。
这个节点模拟它：不断往 /odin1/pointcloud 话题发布点云数据。

【FAE 视角】
真实 Odin1 用 C++ SDK 发布真正的传感器数据，
但**数据格式完全一样**（都是 PointCloud2 消息）。
所以你在 RViz 里看到的效果 = 将来接真设备看到的效果。

【Odin1 真实参数对照】
- 本例：400 个点，2 Hz（为了看得清、不卡）
- 真机：最高 700,000 点/秒，15 FPS
"""

import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2


class FakeOdin(Node):
    """模拟 Odin1 的发布者节点"""

    def __init__(self):
        super().__init__('fake_odin')

        # 发布到 Odin1 风格的话题名
        self.publisher_ = self.create_publisher(
            PointCloud2, '/odin1/pointcloud', 10)

        # 每 0.5 秒发一帧
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.frame = 0

    def timer_callback(self):
        # 生成一片点云（20 x 20 = 400 个点），模拟扫描到的一面墙
        points = []
        for i in range(20):
            for j in range(20):
                x = i * 0.05 - 0.5          # 横向 -0.5 ~ +0.5 米
                y = j * 0.05 - 0.5          # 纵向
                # 让表面像波浪一样起伏（这样能看出数据在动）
                z = math.sin(i * 0.3 + self.frame * 0.2) * 0.05
                points.append([x, y, z])

        # 消息头：时间戳 + 坐标系名
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = 'odin1_link'      # ← RViz 里要用到这个名字！

        # 把点列表打包成 PointCloud2 消息
        cloud = point_cloud2.create_cloud_xyz32(header, points)
        self.publisher_.publish(cloud)

        self.get_logger().info(
            f'发布点云: {len(points)} 个点（第 {self.frame} 帧）')
        self.frame += 1


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(FakeOdin())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
