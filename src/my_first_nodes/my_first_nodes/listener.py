"""
listener.py —— 订阅者（Subscriber）

作用：监听 "chatter" 话题，一有消息就打印出来。

【FAE 视角】
将来你的客户程序（比如导航算法）就是这么接收 Odin1 数据的：
  订阅 /odin1/pose 拿到位姿 → 送给路径规划模块
本程序只是把"位姿"换成了字符串，机制完全一样。

【排障价值】
客户端收不到数据时，第一个要跑的就是订阅端——
如果这里能看到数据，说明传感器没问题，问题在客户自己的程序。
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    """一个订阅者节点"""

    def __init__(self):
        super().__init__('listener')

        # 创建订阅者：
        #   参数1 消息类型   —— 必须和发布者一致
        #   参数2 话题名     —— 必须和发布者一致，这是它们"对上暗号"的关键
        #   参数3 回调函数   —— 收到消息就自动调用它
        #   参数4 队列长度
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        """每收到一条消息，这个函数就被自动调用一次"""
        self.get_logger().info(f'收到: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = Listener()

    # 同样保持运行，等待消息进来
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
