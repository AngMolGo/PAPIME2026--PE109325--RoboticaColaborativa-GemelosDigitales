import json
import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen
from PyQt6.QtCore import Qt

class ConnectionLED(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(20, 20)
        self.connected = False
        
    def set_connected(self, state):
        self.connected = state
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor("#00FF00") if self.connected else QColor("#AA0000")
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawEllipse(2, 2, 16, 16)


class TopBar(QFrame):
    ip_changed = pyqtSignal(str)
    
    def __init__(self, config_path="config.json", parent=None):
        super().__init__(parent)
        self.config_path = config_path
        self.ip_address = "127.0.0.1"
        
        self.setStyleSheet("""
            TopBar {
                background-color: #d4d3d2;
                border-bottom: 2px solid #aaa;
            }
        """)
        
        self.load_config()
        self.init_ui()
        
    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.ip_address = data.get("Network", {}).get("IP", "127.0.0.1")
            except Exception as e:
                print(f"Error loading config: {e}")
                
    def save_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
            except Exception:
                data = {}
        else:
            data = {}
            
        if "Network" not in data:
            data["Network"] = {}
        data["Network"]["IP"] = self.ip_address
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.led = ConnectionLED()
        
        lbl = QLabel("Controlador IP:")
        lbl.setStyleSheet("font-weight: bold;")
        
        self.ip_input = QLineEdit(self.ip_address)
        self.ip_input.setReadOnly(True)
        self.ip_input.setFixedWidth(150)
        self.ip_input.setStyleSheet("""
            QLineEdit {
                background-color: #E0E0E0;
                border: 1px solid gray;
                border-radius: 4px;
                padding: 2px;
            }
            QLineEdit[readOnly="false"] {
                background-color: #FFFFFF;
                border: 2px solid #0055AA;
            }
        """)
        
        self.btn_edit = QPushButton("✏️ Editar")
        self.btn_edit.setCheckable(True)
        self.btn_edit.setFixedWidth(80)
        self.btn_edit.toggled.connect(self.on_edit_toggled)
        
        layout.addWidget(self.led)
        layout.addWidget(lbl)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.btn_edit)
        layout.addStretch()

    def on_edit_toggled(self, checked):
        self.ip_input.setReadOnly(not checked)
        self.ip_input.style().unpolish(self.ip_input)
        self.ip_input.style().polish(self.ip_input)
        
        if checked:
            self.btn_edit.setText("💾 Guardar")
            self.ip_input.setFocus()
        else:
            self.btn_edit.setText("✏️ Editar")
            new_ip = self.ip_input.text().strip()
            if new_ip != self.ip_address:
                self.ip_address = new_ip
                self.save_config()
                self.ip_changed.emit(self.ip_address)
