import time
from rtde_control import RTDEControlInterface
from rtde_io import RTDEIOInterface
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

ROBOT_IP = "192.168.1.3"
config_file = "input_recipe.xml"

conf = rtde_config.ConfigFile(config_file)
input_names, input_types = conf.get_recipe('input')

con = rtde.RTDE(ROBOT_IP, 30004)
con.connect()

# preparar input recipe
con.send_input_setup(input_names, input_types)
inputs = con.input_data

con.send_start()

# ---- ENCENDER ----
inputs.input_bit_register_0 = True
con.send(input=inputs)
time.sleep(0.1)

# ---- APAGAR ----
inputs.input_bit_register_0 = False
con.send(input=inputs)
time.sleep(0.1)

con.send_pause()
con.disconnect()
