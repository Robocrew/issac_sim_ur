from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_moveit_rviz_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("ur", package_name="moveit_config").to_moveit_configs()
    # MoveGroup owns planning configuration; passing it to RViz causes a
    # parameter type conflict when the Motion Planning display reloads it.
    moveit_config.joint_limits = {}
    moveit_config.robot_description_kinematics = {}
    return generate_moveit_rviz_launch(moveit_config)
