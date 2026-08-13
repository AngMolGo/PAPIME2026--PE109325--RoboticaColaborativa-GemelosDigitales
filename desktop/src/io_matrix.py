from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem, QGraphicsPathItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QBrush, QPen, QPainterPath, QPainter

class PortItem(QGraphicsRectItem):
    def __init__(self, x, y, name, port_type, parent_matrix, is_source=False):
        super().__init__(x, y, 20, 20)
        self.name = name
        self.port_type = port_type # 'DI', 'DO', 'PWR'
        self.parent_matrix = parent_matrix
        self.is_source = is_source
        
        self.setBrush(QBrush(QColor("black")))
        self.setPen(QPen(Qt.GlobalColor.gray, 2))
        
        # Add label next to port
        self.label = QGraphicsTextItem(self.name, self)
        # Position label based on side
        self.label.setPos(x - 35 if len(self.name) > 2 else x - 25, y - 2)

    def set_active(self, active):
        if active:
            if self.port_type == 'DO':
                self.setBrush(QBrush(QColor("yellow")))
            else:
                self.setBrush(QBrush(QColor("black")))
        else:
            self.setBrush(QBrush(QColor("black")))

    def mousePressEvent(self, event):
        self.parent_matrix.port_clicked(self)
        super().mousePressEvent(event)

class WireItem(QGraphicsPathItem):
    def __init__(self, port1, port2):
        super().__init__()
        self.port1 = port1
        self.port2 = port2
        self.setPen(QPen(QColor("red"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        self.update_path()
        
    def update_path(self):
        p1 = self.port1.rect().center()
        p2 = self.port2.rect().center()
        
        path = QPainterPath(p1)
        c1 = QPointF(p1.x() + 40, p1.y())
        c2 = QPointF(p2.x() - 40, p2.y())
        path.cubicTo(c1, c2, p2)
        self.setPath(path)
        
    def mousePressEvent(self, event):
        self.port1.parent_matrix.remove_wire(self)

class IOMatrix(QGraphicsView):
    def __init__(self, register_manager, parent=None):
        super().__init__(parent)
        self.rm = register_manager
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setBackgroundBrush(QBrush(QColor("#E0E0E0")))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.ports = {}
        self.wires = []
        self.selected_port = None
        
        self.init_ports()
        
        self.rm.data_changed.connect(self.on_data_changed)

    def init_ports(self):
        # Coordinates setup
        start_x = 80
        start_y = 50
        y_step = 35
        
        # Power / Sources (24V)
        for i in range(8):
            p = PortItem(start_x, start_y + i*y_step, "24V", 'PWR', self, is_source=True)
            self.scene.addItem(p)
            
        # Digital Inputs
        for i in range(8):
            name = f"DI{i}"
            p = PortItem(start_x + 80, start_y + i*y_step, name, 'DI', self)
            self.scene.addItem(p)
            self.ports[name] = p
            
        # Digital Outputs
        start_x_out = 280
        for i in range(8):
            name = f"DO{i}"
            p = PortItem(start_x_out, start_y + i*y_step, name, 'DO', self)
            self.scene.addItem(p)
            self.ports[name] = p
            
        # Power / Ground (0V)
        for i in range(8):
            p = PortItem(start_x_out + 80, start_y + i*y_step, "0V", 'PWR', self, is_source=True)
            self.scene.addItem(p)

    def port_clicked(self, port):
        if self.selected_port is None:
            if port.is_source:
                self.selected_port = port
                port.setPen(QPen(QColor("cyan"), 3))
        else:
            # Connect source to DI
            if not port.is_source and port.port_type == 'DI' and self.selected_port.name == "24V":
                existing = [w for w in self.wires if w.port2 == port]
                if not existing:
                    wire = WireItem(self.selected_port, port)
                    self.scene.addItem(wire)
                    self.wires.append(wire)
                    self.rm.set_input(port.name, True)
            
            # Reset selection
            self.selected_port.setPen(QPen(Qt.GlobalColor.gray, 2))
            self.selected_port = None

    def remove_wire(self, wire):
        if wire in self.wires:
            self.scene.removeItem(wire)
            self.wires.remove(wire)
            if wire.port2.port_type == 'DI':
                self.rm.set_input(wire.port2.name, False)

    def on_data_changed(self, data):
        outs = data.get("outputs", {})
        for name, port in self.ports.items():
            if name.startswith("DO"):
                port.set_active(outs.get(name, False))
