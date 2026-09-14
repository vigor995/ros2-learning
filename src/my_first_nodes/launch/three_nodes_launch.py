"""
three_nodes_launch.py —— 一次性启动多个节点的"启动文件"

【为什么需要它】
真实机器人有几十个节点（传感器、定位、导航、控制...），
不可能开几十个终端一个个敲。Launch 文件就是"批量启动清单"。

【FAE 视角】
Odin1 的官方 SDK 一定会提供类似的 launch 文件，
一条命令就能启动"模组驱动 + 建图 + 可视化"整套系统。
学会看懂/修改 launch 文件 = 能给客户做定制化部署。

【用法】
ros2 launch my_first_nodes three_nodes_launch.py
按一次 Ctrl+C → 所有节点一起停
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # 发布者：往外发数据
        Node(
            package='my_first_nodes',      # 哪个功能包
            executable='talker',           # 哪个可执行文件
            name='talker',                 # 节点名（可省略，默认同 executable）
            output='screen',               # 输出直接打到终端（方便看日志）
        ),

        # 订阅者①
        Node(
            package='my_first_nodes',
            executable='listener',
            name='listener',
            output='screen',
        ),

        # 订阅者②
        Node(
            package='my_first_nodes',
            executable='spy',
            name='spy',
            output='screen',
        ),
    ])
