import json
import os
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class RegisterManager(QObject):
    data_changed = pyqtSignal(dict)
    
    def __init__(self, filepath="registers.json", parent=None):
        super().__init__(parent)
        self.filepath = filepath
        self.data = {"inputs": {}, "outputs": {}}
        self.last_mtime = 0
        self.load_data()
        
        # Polling for external changes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_file)
        self.timer.start(200) # 200 ms
        
    def load_data(self):
        if os.path.exists(self.filepath):
            try:
                mtime = os.path.getmtime(self.filepath)
                if mtime > self.last_mtime:
                    with open(self.filepath, 'r') as f:
                        self.data = json.load(f)
                    self.last_mtime = mtime
                    self.data_changed.emit(self.data)
            except Exception as e:
                print(f"Error reading JSON: {e}")
        else:
            self.save_data()
            
    def save_data(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
            self.last_mtime = os.path.getmtime(self.filepath)
        except Exception as e:
            print(f"Error writing JSON: {e}")
            
    def check_file(self):
        self.load_data()
        
    def set_input(self, key, value):
        if self.data["inputs"].get(key) != value:
            self.data["inputs"][key] = value
            self.save_data()

    def get_output(self, key):
        return self.data["outputs"].get(key, False)

    def set_output(self, key, value):
        if self.data["outputs"].get(key) != value:
            self.data["outputs"][key] = value
            self.save_data()
            self.data_changed.emit(self.data)
