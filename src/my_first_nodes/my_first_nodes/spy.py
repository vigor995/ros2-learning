import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Spy(Node):
    def __init__(self):
        super().__init__('spy')
        self.create_subscription(String, 'chatter', self.cb, 10)
    def cb(self, msg):
        self.get_logger().info(f'   [间谍] 偷听到: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Spy())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
