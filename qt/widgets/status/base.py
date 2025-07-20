from PyQt5.QtWidgets import QStatusBar, QLabel

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color: #212327;')
        self.setContentsMargins(10, 0, 10, 0)  
        self._set_widgets()

    def _set_widgets(self):
        # Connection status label
        self.connection_label = QLabel('Статусбар. Здесь будет отображать свякую ересь')
        self.addWidget(self.connection_label) 
