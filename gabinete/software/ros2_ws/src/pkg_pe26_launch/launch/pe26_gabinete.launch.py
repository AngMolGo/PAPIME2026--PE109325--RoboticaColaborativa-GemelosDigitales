# Módulo para el launch file
from launch import LaunchDescription

# Módulos para sustituciones e incluir launches de otros paquetes
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

# Módulo para incorporar Nodos
from launch_ros.actions import Node


# Función que busca ros_launch para ejecutar el launch
def generate_launch_description():

    # Retorna una instancia de LaunchDescription, 
    # esta instancia lleva la información de los programas que va a correr el launchfile.
    return LaunchDescription([
        
        IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('ur_robot_driver'),
                'launch',
                'ur_control.launch.py'
            ]),
            launch_arguments={
                'ur_type': 'ur5e',
                'robot_ip': '192.168.1.3',
                'launch_rviz': 'false',
            }.items()
        ),

        Node(
            package='pkg_pe26_gabinete',
            namespace='pkg_pe26_gabinete',
            executable='translate_node',
            name='translate_node'
        )

        #Node(
        #    package='pkg_pe26_gabinete',
        #    namespace='pkg_pe26_gabinete',
        #    executable='translate_node',
        #    name='translate_node'
        #)

    ])