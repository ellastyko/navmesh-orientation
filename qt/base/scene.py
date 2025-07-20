import numpy as np
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtCore import QPoint
from OpenGL.GL import *
from OpenGL.GLU import *

class BaseGLWidget(QGLWidget):
    zoom = 0
    rotate_x = 0
    rotate_z = 0

    AXES = True
    HUD  = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        # Загрузка и подготовка изображения
        self.last_pos = QPoint()
    
    def _init_ui(self):
        self.setStyleSheet("""
            border-radius: 5px;
            background-color: #303030;
            color: white;
        """)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glShadeModel(GL_SMOOTH)  # Включаем сглаживание
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        glClearColor(0.53, 0.81, 0.98, 1.0)

        # Освещение
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
        glMaterialf(GL_FRONT, GL_SHININESS, 30)
        glEnable(GL_COLOR_MATERIAL)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Управление камерой
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rotate_x, 1, 0, 0)
        glRotatef(self.rotate_z, 0, 0, 1)

        # Источник света
        glLightfv(GL_LIGHT0, GL_POSITION, [5, 10, 5, 1])

        # Оси координат
        if self.AXES is True:
            self.draw_axes(1500)

        self.paint()

        # HUD
        if self.HUD is True:
            self.draw_hud()

    def paint(self):
        pass

    def draw_sphere(self, radius, slices, stacks):
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, slices, stacks)
        gluDeleteQuadric(quadric)

    def draw_polygon(self, corners, fill_color=(0.2, 0.4, 0.8, 0.7), edge_color=(1.0, 1.0, 1.0, 1.0), draw_edges=True, is_selected=False):
        """
        Рисует полигон по заданным углам.
        
        Args:
            corners (list): Список словарей с ключами 'X', 'Y', 'Z'.
            color (tuple): RGB-цвет линии (по умолчанию белый).
        """
         # Сначала рисуем заливку
        if fill_color:
            glColor4f(*fill_color)
            glBegin(GL_POLYGON)
            for corner in corners:
                glVertex3f(corner['X'], corner['Y'], corner['Z'])
            glEnd()
        
        # Затем рисуем границы
        if draw_edges and edge_color:
            glColor4f(*edge_color)
            glLineWidth(2.0)  # Толщина линии
            glBegin(GL_LINE_LOOP)
            for corner in corners:
                glVertex3f(corner['X'], corner['Y'], corner['Z'])
            glEnd()
        self.update()
    
    def draw_connections(self, areas, color=(1.0, 0.0, 0.0)):
        """
        Рисует соединения между областями.
        
        Args:
            areas (list): Список всех областей.
            color (tuple): RGB-цвет соединений (по умолчанию красный).
        """
        centers = {}
        
        # Вычисляем центры всех областей
        for area in areas:
            corners = area['Corners']
            x = np.mean([c['X'] for c in corners])
            y = np.mean([c['Y'] for c in corners])
            z = np.mean([c['Z'] for c in corners])
            centers[area['ID']] = (x, y, z)
        
        # Рисуем соединения
        glColor3f(*color)
        glBegin(GL_LINES)
        for area in areas:
            if 'Connections' in area:
                for conn in area['Connections']:
                    target_id = conn['TargetArea']
                    if area['ID'] in centers and target_id in centers:
                        x1, y1, z1 = centers[area['ID']]
                        x2, y2, z2 = centers[target_id]
                        glVertex3f(x1, y1, z1)
                        glVertex3f(x2, y2, z2)
        glEnd()

    def draw_axes(self, length):
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)  # X
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)  # Y
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)  # Z
        glEnd()

    def draw_hud(self):
        self.renderText(10, 20, f"Rotation: X={self.rotate_x:.1f}° Y={self.rotate_z:.1f}°")
        self.renderText(10, 40, f"Zoom: Z={self.zoom:.1f}°")
        self.renderText(10, 60, "Controls: LMB - rotate, Wheel - zoom")

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.2
        self.update()

    def cleanup(self):
        self.makeCurrent()
        # Очисти буферы, текстуры, выделенную память
        self.doneCurrent()