import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    pkg_name = "moveit_config"
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Load full MoveIt 2 configuration
    moveit_config = (
        MoveItConfigsBuilder("ur", package_name="moveit_config")
        .robot_description(file_path="config/ur.urdf.xacro")
        .robot_description_semantic(file_path="config/ur.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
)

    ros2_controllers_path = os.path.join(pkg_share, "config", "ros2_controllers.yaml")

    # Keep MoveGroup params valid for the planning node, while avoiding the
    # RViz reload issue caused by passing kinematic/joint-limit parameters back
    # to the motion-planning panel.
    move_group_params = moveit_config.to_dict()
    move_group_params.setdefault("robot_description_planning", {})

    # 2. Start the ros2_control node (TopicBasedSystem communicating with Isaac Sim)
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description,
            ros2_controllers_path
        ],
        output="screen",
    )

    # 3. Robot State Publisher (Publishes /tf from /joint_states)
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            {"ignore_timestamp": True},
        ],
    )

    # 4. Spawner: joint_state_broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    # 5. Spawner: joint_trajectory_controller
    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", "--controller-manager", "/controller_manager"],
        output="screen",
    )

    # 6. MoveIt 2 core planning node (move_group)
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[move_group_params],
    )

    # 7. RViz visualization
    rviz_config_file = os.path.join(pkg_share, "config", "moveit.rviz")
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
        ],
    )

    return LaunchDescription([
        control_node,
        robot_state_publisher_node,
        joint_state_broadcaster_spawner,
        joint_trajectory_controller_spawner,
        move_group_node,
        rviz_node,
    ])