# Módulo para el launch file
from launch import LaunchDescription

# Módulos para sustituciones e incluir launches de otros paquetes
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

# Módulo para incorporar Nodos
from launch_ros.actions import Node


# Función que busca ros_launch para ejecutar el launch
def generate_launch_description():

    # Construimos la ruta usando Sustituciones (evaluado en tiempo de ejecución)

    # Creamos la acción de inclusión
    include_other_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
                                      FindPackageShare('pkg_ur_controller'),
                                      'launch',
                                      'ur_servo_bridge.launch.py'
                                    ]))#,
        #launch_arguments={
        #    'parametro_1': 'valor_1',
        #    'use_sim_time': 'true'
        #}.items()
    )

    # Retorna una instancia de LaunchDescription, 
    # esta instancia lleva la información de los programas que va a correr el launchfile.
    return LaunchDescription([
        include_other_launch
    ])