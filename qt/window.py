from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QDockWidget
from PyQt5.QtCore import Qt
from configurator import config
from qt.widgets.status import StatusBar
from qt.widgets.main import MainWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        # GUI элементы
        self.setup_ui()

    def _init_ui(self):
        self.setWindowTitle(config['main']['appname'])
        self.setStyleSheet("background-color: #292A2D; color: #f8faff;")

        windowcfg = config['window']
        l_indent, t_indent = windowcfg['indent']
        self.setGeometry(l_indent, t_indent, windowcfg['width'], windowcfg['height'])
        self.setMinimumSize(windowcfg['minw'], windowcfg['minh'])
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        self.mainWidget     = MainWidget()
        layout.addWidget(self.mainWidget, stretch=7)

        # self.dockw = SidebarDock('Controller', self)
        # self.dockw.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        # self.addDockWidget(Qt.RightDockWidgetArea, self.dockw)
        # self.dockw.setContextMenuPolicy(Qt.PreventContextMenu)

        # Статус бар
        status_bar = StatusBar()
        self.setStatusBar(status_bar)
    
    def closeEvent(self, event):
        super().closeEvent(event)