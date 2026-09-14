"""
talker.py —— 发布者（Publisher）

作用：每秒往 "chatter" 这个话题上发一条消息。

【FAE 视角】
Odin1 在机器人里扮演的就是这个角色！它不断往话题上发：
  - /odin1/pointcloud   点云数据
  - /odin1/imu          IMU 数据
  - /odin1/pose         位姿数据
本程序只是把"点云"换成了简单的字符串，原理完全一样。
"""

import rclpy                      # ROS 2 的 Python 客户端库
from rclpy.node import Node       # 节点基类
from std_msgs.msg import String   # 标准字符串消息类型


class Talker(Node):
    """一个发布者节点"""

    def __init__(self):
        # 调用父类构造，并给节点起名叫 'talker'
        # 节点名在整个 ROS 网络里必须唯一
        super().__init__('talker')

        # 创建发布者：往 'chatter' 话题发 String 类型的消息
        # 第二个参数 10 是"队列长度"：如果订阅者处理慢了，最多缓存 10 条
        # 【对应 Odin1】它也是这样 create_publisher(PointCloud2, '/odin1/pointcloud', 10)
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # 创建定时器：每 0.5 秒触发一次 timer_callback
        # 【对应 Odin1】点云是 15Hz（约 0.067 秒一次），位姿最高 1000Hz
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # 计数器，用来让每条消息不一样
        self.i = 0

    def timer_callback(self):
        """定时器到点就会执行这个函数"""
        msg = String()                          # 创建一个消息对象
        msg.data = f'Odin1 pose frame: {self.i}'     # 往消息里填数据

        self.publisher_.publish(msg)            # 发布！

        # 打印日志（会显示在终端里）
        self.get_logger().info(f'发布: "{msg.data}"')

        self.i += 1                             # 计数 +1


def main(args=None):
    rclpy.init(args=args)      # 初始化 ROS 2 通信
    node = Talker()            # 创建我们的节点

    # spin = 让节点保持运行，不断处理回调（定时器、收到的消息等）
    # 这行会一直阻塞，直到你按 Ctrl+C
    rclpy.spin(node)

    # 收尾：销毁节点、关闭 ROS
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
