from PyQt5.QtWidgets import QWidget, QVBoxLayout
from OpenGL.GL import *
from OpenGL.GLU import *
from .scene import SceneWidget

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.scene_widget = SceneWidget()
        layout.addWidget(self.scene_widget, stretch=10)

    def closeEvent(self, event):
        self.scene_widget.cleanup()
        event.accept()