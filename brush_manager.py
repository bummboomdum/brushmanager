from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class BrushManagerDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pinsel Manager")
        
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        self.table = QTableView()
        layout.addWidget(self.table)
        
        btn = QPushButton("Bundle erstellen")
        layout.addWidget(btn)
        
        main_widget.setLayout(layout)
        self.setWidget(main_widget)
        
    def canvasChanged(self, canvas):
        pass