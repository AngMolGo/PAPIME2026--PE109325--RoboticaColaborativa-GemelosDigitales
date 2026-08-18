#!/usr/bin/env python3

import socket # Para mandar comando a puerto 30003 (RTDE)

# # # Módulos (dependencias) # # #
import rclpy                    # Importa ROS Client Library para Python.
from rclpy.node import Node     # Importa la clase Node para la creación de nodos.

from pkg_pe26_gabinete_custom_interfaces.msg import Outputs
from pkg_pe26_gabinete_custom_interfaces.msg import Inputs
from ur_msgs.msg import IOStates

# # # Definición de nuestra clase Nodo (Publicador) # # #

# Se define una clase "Nodo_Saludador" que hereda de la clase padre Node, antes importada.
class Nodo_Saludador(Node):

    def __init__(self):
        
        super().__init__('driver_traductor') # Inicialización como se tratara de la clase padre, se crea un nodo con el nombre "nodo_saludador".
        
        self.robotIP = "192.168.1.3"
        self.REALTIME_PORT = 30003

        self.publisher_ = self.create_publisher(
            Outputs,
            '/gabinete/outputs/standard',
            10) # Crea un "publicador", una parte del nodo que publica en el tópico. Indica que publicará mensajes de tipo String (clase importada) a un topico llamado "saludos". (10 es el tamaño del queue)

        self.publisher_2 = self.create_publisher(
                    Outputs,
                    '/gabinete/outputs/config',
                    10) # Crea un "publicador", una parte del nodo que publica en el tópico. Indica que publicará mensajes de tipo String (clase importada) a un topico llamado "saludos". (10 es el tamaño del queue)

        self.subscription = self.create_subscription(
            IOStates,
            '/io_and_status_controller/io_states',
            self.listener_callback,
            10) # Crea un "suscriptor", una parte del nodo que tiene entrada del tópico. Indica que se suscribirá a mensajes de tipo String (clase importada) de un topico llamado "saludos". (10 es el tamaño del queue). Cada vez que escuche un mensaje ejecutará la función "listener_callback".
        self.subscription  # prevent unused variable warning

        self.subscription_2 = self.create_subscription(
            Inputs,
            '/gabinete/inputs/standard',
            self.listener_callback_inputs,
            10) # Crea un "suscriptor", una parte del nodo que tiene entrada del tópico. Indica que se suscribirá a mensajes de tipo String (clase importada) de un topico llamado "saludos". (10 es el tamaño del queue). Cada vez que escuche un mensaje ejecutará la función "listener_callback".
        self.subscription_2  # prevent unused variable warning

        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback) # Se creará un timer, que llamará a la función callback, cada periodo de tiempo de 0.5s. Es un servico de timer que ejecuta una función "callback".

        self.__io_states = IOStates()

    def timer_callback(self):
        msg = Outputs() # Clase String importada
        msg_2 = Outputs() # Clase String importada

        output_states = self.__io_states.digital_out_states

        for output in output_states:
            if output.pin < 8:
                msg.output[output.pin] = output.state
            if 8 <= output.pin and output.pin < 16:
                msg_2.output[output.pin-8] = output.state
        
        self.publisher_.publish(msg) # Se llama al método del publicador que publica una instancia de la clase String con el mensaje.
        self.publisher_2.publish(msg_2) # Se llama al método del publicador que publica una instancia de la clase String con el mensaje.
        
        self.get_logger().info(f'Publishing: "{msg.output}"') # El nodo arroja un log, diciendo que se está publicando un tópico con el mensaje deseado.
        self.get_logger().info(f'Publishing2: "{msg_2.output}"') # El nodo arroja un log, diciendo que se está publicando un tópico con el mensaje deseado.
        

    def listener_callback(self, msg): # Uno de los parámetros de la función es el mensaje recibido en el tópico.
        self.__io_states = msg
        #self.get_logger().info(f'I heard: "{msg.digital_out_states}"') # Cada vez que "escuche" un mensaje del tópico, indicará con un log el mensaje recibido.

    def listener_callback_inputs(self, msg): # Uno de los parámetros de la función es el mensaje recibido en el tópico.
        #"set_digital_out(5, True)\n"
        for i in range(0,8):
            try:
                # Appends new line to the URScript command (the command will not execute without this)
                input = msg.input[i]
                
            except:
                print("Algo salió mal")

        self.get_logger().info(f'I heard: "{msg}"') # Cada vez que "escuche" un mensaje del tópico, indicará con un log el mensaje recibido.

    def iniciarComunicacion(self):
        try:
            # Create a socket connection with the robot IP and port number defined above
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.robotIP, self.REALTIME_PORT))
        except Exception as e:
            print(f"An error occurred: {e}")

    def cerrarComunicacion(self):
        try:
            # Close the connection
            self.s.close()
        except Exception as e:
            print(f"An error occurred: {e}")

# # # # # # # # # FUNCIÓN PRINCIPAL DEL PROGRAMA # # # # # # # # # #

# Función principal del programa
def main(args=None):
    rclpy.init(args=args) # Inicializa la comunicación con el sistema de comunicación de ROS2. 

    nodo_saludador = Nodo_Saludador() # Se crea una instancia de la clase desarrollada.

    rclpy.spin(nodo_saludador) # Mantiene un bucle que permite mantener al nodo nodo_saludador "vivo". 

    # Se mantiene vivo hasta que se destruye, ya sea por un error en el código, una destrucción programada o por orden del usuario. Por ejemplo, cuando se ejecuta ctrl+c en la terminal.

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    nodo_saludador.destroy_node() # Cuando se acaba el bucle se autodestruye el nodo.
    rclpy.shutdown() # Termina la sesión de comunicación con el entorno ROS2.

# "Buenas prácticas" para scripts de python.
if __name__ == '__main__':
    main()

    