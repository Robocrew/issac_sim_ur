from moveit_configs_utils import MoveItConfigsBuilder
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("ur", package_name="moveit_config").to_moveit_configs()
    return LaunchDescription(
        [
            DeclareLaunchArgument("publish_frequency", default_value="100.0"),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                respawn=True,
                output="screen",
                parameters=[
                    moveit_config.robot_description,
                    {"publish_frequency": LaunchConfiguration("publish_frequency")},
                ],
            ),
        ]
    )
