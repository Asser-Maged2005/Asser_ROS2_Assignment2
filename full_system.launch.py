import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('arm_description')
    port_arg = DeclareLaunchArgument('port', default_value='/dev/ttyUSB0')

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'sim.launch.py')
        )
    )

    serial_bridge = Node(
        package='arm_control',
        executable='serial_bridge',
        parameters=[{'port': LaunchConfiguration('port'), 'baudrate': 115200}],
        output='screen',
    )

    arm_gui = TimerAction(
        period=3.0,
        actions=[
            Node(
                package='arm_control',
                executable='arm_gui',
                output='screen',
            )
        ],
    )

    return LaunchDescription([port_arg, sim_launch, serial_bridge, arm_gui])
