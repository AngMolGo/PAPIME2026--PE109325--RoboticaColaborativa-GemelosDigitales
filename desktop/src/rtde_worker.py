import os
import time
from PyQt6.QtCore import QThread, pyqtSignal

try:
    import rtde.rtde as rtde
    import rtde.rtde_config as rtde_config
    UR_RTDE_AVAILABLE = True
except ImportError as e:
    print(f"No se encontro el cliente oficial RTDE: {e}")
    UR_RTDE_AVAILABLE = False

class RTDEWorker(QThread):
    connected_signal = pyqtSignal(bool)
    
    def __init__(self, ip_address, register_manager, parent=None):
        super().__init__(parent)
        self.ip_address = ip_address
        self.rm = register_manager
        self.running = True
        
        self.con = None
        self.is_connected = False
        
        self.setp = None # Variables de escritura
        self.current_bitmask = 0
        
        self.rm.data_changed.connect(self.on_local_data_changed)
        # Llamar manualmente una vez para sincronizar estado inicial
        self.on_local_data_changed(self.rm.data)

    def update_ip(self, new_ip):
        self.ip_address = new_ip
        self.disconnect_rtde()

    def disconnect_rtde(self):
        if self.con:
            try:
                self.con.disconnect()
            except:
                pass
        self.con = None
        if self.is_connected:
            self.is_connected = False
            self.connected_signal.emit(False)

    def run(self):
        if not UR_RTDE_AVAILABLE:
            print("Cliente UR RTDE no disponible. Ejecutando en simulacion offline.")

        config_file = os.path.join(os.path.dirname(__file__), "..", "rtde_config.xml")

        while self.running:
            if not UR_RTDE_AVAILABLE:
                time.sleep(1)
                continue

            try:
                if not self.is_connected:
                    self.con = rtde.RTDE(self.ip_address, 30004)
                    self.con.connect()
                    
                    # Cargar XML configuration
                    conf = rtde_config.ConfigFile(config_file)
                    state_names, state_types = conf.get_recipe('state')
                    setp_names, setp_types = conf.get_recipe('setp')
                    
                    # Setup output and input
                    self.con.send_output_setup(state_names, state_types, frequency=10)
                    self.setp = self.con.send_input_setup(setp_names, setp_types)
                    
                    if not self.con.send_start():
                        raise Exception("Fallo al iniciar sincronizacion RTDE")
                        
                    self.is_connected = True
                    self.connected_signal.emit(True)
                
                # Recibir estado del robot
                state = self.con.receive()
                if state is None:
                    raise Exception("Conexion perdida (receive devolvio None)")
                    
                # Leer las salidas del robot y mandarlas a la matriz I/O (DO0 a DO7)
                for i in range(8):
                    bit_val = bool((state.actual_digital_output_bits >> i) & 1)
                    self.rm.set_output(f"DO{i}", bit_val)

                # Leer las salidas configurables (CO0 a CO5) mapeadas en los bits 8 a 13
                self.rm.set_output("tower_red", bool((state.actual_digital_output_bits >> 8) & 1))
                self.rm.set_output("tower_yellow", bool((state.actual_digital_output_bits >> 9) & 1))
                self.rm.set_output("tower_green", bool((state.actual_digital_output_bits >> 10) & 1))
                
                self.rm.set_output("out_btn_green", bool((state.actual_digital_output_bits >> 11) & 1))
                self.rm.set_output("out_btn_red", bool((state.actual_digital_output_bits >> 12) & 1))
                self.rm.set_output("out_btn_blue", bool((state.actual_digital_output_bits >> 13) & 1))

                # Escribir nuestras entradas hacia el robot (en el mismo hilo)
                if self.setp is not None:
                    self.setp.input_bit_register_64 = int((self.current_bitmask >> 0) & 1)
                    self.setp.input_bit_register_65 = int((self.current_bitmask >> 1) & 1)
                    self.setp.input_bit_register_66 = int((self.current_bitmask >> 2) & 1)
                    self.setp.input_bit_register_67 = int((self.current_bitmask >> 3) & 1)
                    self.setp.input_bit_register_68 = int((self.current_bitmask >> 4) & 1)
                    self.setp.input_bit_register_69 = int((self.current_bitmask >> 5) & 1)
                    self.setp.input_bit_register_70 = int((self.current_bitmask >> 6) & 1)
                    self.setp.input_bit_register_71 = int((self.current_bitmask >> 7) & 1)
                    self.setp.input_bit_register_72 = int((self.current_bitmask >> 8) & 1)
                    self.setp.input_bit_register_73 = int((self.current_bitmask >> 9) & 1)
                    self.setp.input_bit_register_74 = int((self.current_bitmask >> 10) & 1)
                    self.setp.input_bit_register_75 = int((self.current_bitmask >> 11) & 1)
                    self.setp.input_bit_register_76 = int((self.current_bitmask >> 12) & 1)
                    self.con.send(self.setp)
            except Exception as e:
                if self.is_connected:
                    print(f"Error en RTDEWorker: {e}")
                    self.disconnect_rtde()
                time.sleep(2.0)

    def on_local_data_changed(self, data):
        inputs = data.get("inputs", {})
        
        # Mapeamos nuestros bools a un bitmask entero
        bitmask = 0
        
        # DI0-DI7 (Bits 0 a 7)
        for i in range(8):
            if inputs.get(f"DI{i}", False):
                bitmask |= (1 << i)
                
        # Botones (ejemplo: Bits 8, 9, 10, 11, 12)
        if inputs.get("btn_green", False): bitmask |= (1 << 8)
        if inputs.get("btn_red", False):   bitmask |= (1 << 9)
        if inputs.get("btn_blue", False):  bitmask |= (1 << 10)
        if inputs.get("estop", False):     bitmask |= (1 << 11)
        if inputs.get("switch", False):    bitmask |= (1 << 12)
        
        # Guardar en memoria para que el worker lo recoja y envie
        self.current_bitmask = bitmask

    def stop(self):
        self.running = False
        self.disconnect_rtde()
        self.wait()
