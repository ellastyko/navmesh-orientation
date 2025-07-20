import os, math, json, logging, cv2
from qt.base.scene import BaseGLWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from utils.map import MapManager

class SceneWidget(BaseGLWidget):
    areas = []

    POINT_SIZE = 4
    dots = []
    connections = []

    def __init__(self, parent=None):
        super().__init__(parent)
        # Map uploading
        self.upload_map('cs_italy')
        self.set_map()
    
    def upload_map(self, mapname):
        # Set map data
        self.currentMap, self.mapdata = mapname, MapManager.get_map(mapname)
        self.set_viewpoint()

    def set_map(self):
        # Clear old data
        self.set_viewpoint()
        self.clear_areas()
        self.clear_dots_data()
        
        self.set_areas()
    
    def set_viewpoint(self):
        # Update map viewpoint
        viewdata = self.mapdata['view']
        self.camera_pos = viewdata['camera']['position']
        self.rotate_x, self.rotate_z = viewdata['rotation']['x'], viewdata['rotation']['z']
        self.zoom = viewdata['camera']['zoom']

    def set_areas(self):
        # Fill data 
        self.clear_dots_data()
        self.clear_areas()

        self.areas = self.mapdata['nav']['Areas']
        
    def clear_dots_data(self):
        # Reset all dots and connections
        self.dots = []
        self.dots_data = []
        self.connections = []
        self.selected_dot = None

    def clear_areas(self):
        self.areas = []

    def paint(self):
        # Отрисовка соединений между areas
        self.draw_connections(self.areas)
        
        for area in self.areas:
            self.draw_polygon(area['Corners'], )  # Голубой цвет

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            dx = event.x() - self.last_pos.x()
            dz = event.y() - self.last_pos.y()
            self.rotate_z += dx * 0.5
            self.rotate_x += dz * 0.5
            self.last_pos = event.pos()
            self.update()