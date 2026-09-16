"""
odin_demo_launch.py —— 一键启动「Odin1 模拟器」整套系统

【为什么需要它】
以前：4 个长驻进程散在 4 个终端里（点云 / 动态TF / 静态TF / RViz）。
      忘开一个 → 半个系统活着；复用终端 → 误杀进程。
现在：一条命令起全部，Ctrl+C 一停全停。

【四个部件】
1. static_transform_publisher   静态TF：base_link → odin1_link（Odin1 装在哪）
2. odin_pose_tf                 动态TF：map → base_link（机器人在走）
3. fake_odin                    点云：模拟 Odin1 的扫描输出
4. rviz2                        可视化：自动加载 odin_demo.rviz

【用法】
ros2 launch my_first_nodes odin_demo_launch.py
Ctrl+C → 全部一起停
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # 1. 静态 TF：Odin1 装在机器人前方 0.1m、高 0.3m、下倾 15°
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='odin1_mount',
            arguments=[
                '--frame-id', 'base_link',
                '--child-frame-id', 'odin1_link',
                '--x', '0.1', '--y', '0.0', '--z', '0.3',
                '--roll', '0', '--pitch', '-0.26', '--yaw', '0',
            ],
            output='screen',
        ),

        # 2. 动态 TF：机器人在 map 里绕圈走（50Hz）
        Node(
            package='my_first_nodes',
            executable='odin_pose_tf',
            name='odin_pose_tf',
            output='screen',
        ),

        # 3. 点云：模拟 Odin1 的扫描输出（2Hz）
        Node(
            package='my_first_nodes',
            executable='fake_odin',
            name='fake_odin',
            output='screen',
        ),

        # 3b. 里程计 + 轨迹：导航算法真正吃的输入
        Node(
            package="my_first_nodes",
            executable="odin_odometry",
            name="odin_odometry",
            output="screen",
        ),

        # 4. RViz：自动加载存档配置，不用手配
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', '/home/ros/ros2_ws/odin_demo.rviz'],
            output='screen',
        ),
    ])
