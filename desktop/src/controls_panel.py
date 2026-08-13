from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen

class LightTower(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 180)
        self.states = {"tower_red": False, "tower_yellow": False, "tower_green": False}
        
    def set_state(self, color, state):
        key = f"tower_{color}"
        if key in self.states and self.states[key] != state:
            self.states[key] = state
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        colors = [
            ("tower_red", QColor(255, 0, 0), QColor(80, 0, 0)),
            ("tower_yellow", QColor(255, 200, 0), QColor(80, 60, 0)),
            ("tower_green", QColor(0, 255, 0), QColor(0, 80, 0))
        ]
        
        y = 0
        h = 60
        w = 60
        
        # Draw tower base/background
        painter.setBrush(QBrush(QColor("#333")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(5, 0, w-10, 180)

        for key, color_on, color_off in colors:
            color = color_on if self.states[key] else color_off
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.drawEllipse(10, y+10, w-20, h-20)
            y += h

class ControlsPanel(QWidget):
    def __init__(self, register_manager, parent=None):
        super().__init__(parent)
        self.rm = register_manager
        self.init_ui()
        
        # Connect to rm signals
        self.rm.data_changed.connect(self.on_data_changed)
        self.on_data_changed(self.rm.data)

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # Buttons layout
        btn_layout = QVBoxLayout()
        self.btn_green = self.create_button("btn_green")
        self.btn_red = self.create_button("btn_red")
        self.btn_blue = self.create_button("btn_blue")
        
        btn_layout.addWidget(self.btn_green)
        btn_layout.addWidget(self.btn_red)
        btn_layout.addWidget(self.btn_blue)
        
        # Center layout (Estop and switch)
        center_layout = QVBoxLayout()
        self.btn_estop = QPushButton("E-STOP")
        self.btn_estop.setFixedSize(100, 100)
        self.btn_estop.setCheckable(True)
        self.btn_estop.setStyleSheet("""
            QPushButton {
                background-color: #CC0000;
                color: white;
                border-radius: 50px;
                border: 4px solid #FFD700;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #880000;
                border: 4px solid #AA8800;
            }
        """)
        self.btn_estop.toggled.connect(lambda checked: self.rm.set_input("estop", checked))
        
        self.btn_switch = QPushButton("OFF")
        self.btn_switch.setFixedSize(60, 60)
        self.btn_switch.setCheckable(True)
        self.btn_switch.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #00AA00;
                color: white;
            }
        """)
        self.btn_switch.toggled.connect(self.on_switch_toggled)
        
        center_layout.addWidget(self.btn_estop, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addSpacing(20)
        center_layout.addWidget(self.btn_switch, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Light tower
        self.light_tower = LightTower()
        
        layout.addLayout(btn_layout)
        layout.addLayout(center_layout)
        layout.addWidget(self.light_tower)
        
    def create_button(self, reg_name):
        btn = QPushButton()
        btn.setFixedSize(60, 60)
        btn.pressed.connect(lambda: self.rm.set_input(reg_name, True))
        btn.released.connect(lambda: self.rm.set_input(reg_name, False))
        return btn

    def update_button_light(self, btn, c_off, c_off_p, c_on, c_on_p, is_lit):
        bg_normal = c_on if is_lit else c_off
        bg_pressed = c_on_p if is_lit else c_off_p
        border_normal = "gray"
        
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_normal};
                border-radius: 30px;
                border: 3px solid {border_normal};
            }}
            QPushButton:pressed {{
                background-color: {bg_pressed};
                border: 3px solid {border_normal};
            }}
        """)

    def on_switch_toggled(self, checked):
        self.btn_switch.setText("ON" if checked else "OFF")
        self.rm.set_input("switch", checked)
        
    def on_data_changed(self, data):
        outs = data.get("outputs", {})
        self.light_tower.set_state("red", outs.get("tower_red", False))
        self.light_tower.set_state("yellow", outs.get("tower_yellow", False))
        self.light_tower.set_state("green", outs.get("tower_green", False))
        
        self.update_button_light(self.btn_green, "#2a5a2a", "#1a3a1a", "#55ff55", "#33cc33", outs.get("out_btn_green", False))
        self.update_button_light(self.btn_red, "#5a2a2a", "#3a1a1a", "#ff5555", "#cc3333", outs.get("out_btn_red", False))
        self.update_button_light(self.btn_blue, "#2a2a5a", "#1a1a3a", "#5555ff", "#3333cc", outs.get("out_btn_blue", False))
