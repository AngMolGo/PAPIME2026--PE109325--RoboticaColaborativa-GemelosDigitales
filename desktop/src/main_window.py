from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame
from src.register_manager import RegisterManager
from src.controls_panel import ControlsPanel
from src.io_matrix import IOMatrix
from src.top_bar import TopBar
from src.rtde_worker import RTDEWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI PAPIME - UR IO Simulator")
        self.resize(850, 500)
        
        self.rm = RegisterManager()
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        self.top_bar = TopBar("config.json")
        main_layout.addWidget(self.top_bar)
        
        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left side: IO Matrix
        self.io_matrix = IOMatrix(self.rm)
        content_layout.addWidget(self.io_matrix, stretch=2)
        
        # Add a separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        content_layout.addWidget(line)
        
        # Right side: Controls
        self.controls = ControlsPanel(self.rm)
        content_layout.addWidget(self.controls, stretch=1)
        
        main_layout.addLayout(content_layout)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #d4d3d2;
            }
        """)

        # Initialize RTDE Worker
        self.rtde_worker = RTDEWorker(self.top_bar.ip_address, self.rm)
        self.rtde_worker.connected_signal.connect(self.top_bar.led.set_connected)
        self.top_bar.ip_changed.connect(self.rtde_worker.update_ip)
        self.rtde_worker.start()

    def closeEvent(self, event):
        self.rtde_worker.stop()
        super().closeEvent(event)
