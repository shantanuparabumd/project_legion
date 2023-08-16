import os

import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription,ExecuteProcess,RegisterEventHandler
from launch.event_handlers import OnProcessExit
import launch_ros
from launch_ros.actions import Node
import xacro
import random

# this is the function launch  system will look for


def generate_launch_description():

    ####### DATA INPUT ##########
    urdf_file = 'robotaxi.urdf'
    xacro_file = "robotaxi.urdf.xacro"
    #xacro_file = "box_bot.xacro"
    package_description = "project_legion"
    use_urdf = False
    # Position and orientation
    # [X, Y, Z]
    position = [0.0, 0.0, 0.5]
    # [Roll, Pitch, Yaw]
    orientation = [0.0, 0.0, 0.0]
    # Base Name or robot
    robot_base_name = "robotaxi"
    ####### DATA INPUT END ##########

    if use_urdf:
        # print("URDF URDF URDF URDF URDF URDF URDF URDF URDF URDF URDF ==>")
        robot_desc_path = os.path.join(get_package_share_directory(
            package_description), "robot", urdf_file)
    else:
        # print("XACRO XACRO XACRO XACRO XACRO XACRO XACRO XACRO XACRO XACRO XACRO ==>")
        robot_desc_path = os.path.join(get_package_share_directory(
            package_description), "urdf", xacro_file)

    robot_desc = xacro.process_file(robot_desc_path)
    xml = robot_desc.toxml()

    entity_name = robot_base_name+"-"+str(random.random())

    pkg_share = launch_ros.substitutions.FindPackageShare(package=package_description).find(package_description)

    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')

    # Spawn ROBOT Set Gazebo (Does not spwan robot only communicates with the Gazebo Client)
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=['-entity',
                   entity_name,
                   '-x', str(position[0]), '-y', str(position[1]
                                                     ), '-z', str(position[2]),
                   '-R', str(orientation[0]), '-P', str(orientation[1]
                                                        ), '-Y', str(orientation[2]),
                   '-topic', '/robot_description'
                   ]
    )

    # Publish Robot Desciption in String form in the topic /robot_description
    publish_robot_description = Node(
        package='project_legion',
        executable='robot_description_publisher.py',
        name='robot_description_publisher',
        output='screen',
        arguments=['-xml_string', xml,
                   '-robot_description_topic', '/robot_description'
                   ]
    )

    # Robot State Publisher
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    robot_state_publisher= Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': xml}],
        output="screen"
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )



    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    robot_velocity_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_velocity_controller", "--controller-manager", "/controller_manager"],
    )

    robot_position_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_position_controller", "--controller-manager", "/controller_manager"],
    )

    # Delay start of robot_controller after `joint_state_broadcaster`
    delay_robot_postion_controller_spawner_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[robot_position_controller_spawner],
        )
    )

    # Delay start of robot_controller after `joint_state_broadcaster`
    delay_robot_velocity_controller_spawner_after_joint_state_broadcaster_spawner = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[robot_velocity_controller_spawner],
        )
    )

    # create and return launch description object
    return LaunchDescription(
        [   
            launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='Flag to enable joint_state_publisher_gui'),
            launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                                description='Absolute path to rviz config file'),
            launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
            publish_robot_description,
            joint_state_publisher_node,
            robot_state_publisher,
            spawn_robot,
            joint_state_broadcaster_spawner,
            delay_robot_postion_controller_spawner_after_joint_state_broadcaster_spawner,
            delay_robot_velocity_controller_spawner_after_joint_state_broadcaster_spawner
        ]
    )