from launch import LaunchDescription
from launch.actions import LogInfo
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os
from launch.substitutions import Command
import launch_ros.descriptions
import launch

def generate_launch_description():
    package_description = "project_legion"
    xacro_file = "robotaxi.urdf.xacro"
    entity_name="taxi"


 

    robot_desc_path = os.path.join(get_package_share_directory(
            package_description), "urdf", xacro_file) # Update this with the actual URDF file path
    
    # RVIZ Configuration
    rviz_config_dir = os.path.join(get_package_share_directory(
        package_description), 'rviz', 'robotaxi.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        name='rviz_node',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_dir])
    
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=entity_name,
        parameters=[{'robot_description': launch_ros.descriptions.ParameterValue(launch.substitutions.Command(['xacro ',robot_desc_path]), value_type=str)  }],
        output="screen"
    )

    joint_state_gui=Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen',
        )
    
    return LaunchDescription([
        robot_state_publisher_node,
        rviz_node,
        joint_state_gui,
        
    ])
