cmake_minimum_required(VERSION 3.8)
project(robot_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY meshes robot table_clamp urdf
  DESTINATION share/${PROJECT_NAME}
)

install(
  FILES
    robot_lula.yaml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()