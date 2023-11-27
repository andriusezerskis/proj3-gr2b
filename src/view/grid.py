import time
from typing import Tuple

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView

from model.terrains.land import Land
from model.terrains.water import Water


class Window(QMainWindow):
    def __init__(self, grid_size: Tuple[int, int], grid):
        super().__init__()
        self.setWindowTitle('Simulation 2D')
        self.setGeometry(100, 100, 400, 400)
        self.view = Grid(grid_size, grid)
        self.setCentralWidget(self.view)


class Grid(QGraphicsView):
    def __init__(self, grid_size, grid):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        """self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)"""
        self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.zoom_step = 0.1

        self.size = 2048, 2048
        self.land_pixmap = QPixmap("../assets/textures/land.png")
        self.land_pixmap = self.land_pixmap.scaled(self.size[0], self.size[1])
        self.water_pixmap = QPixmap("../assets/textures/water.png")
        self.water_pixmap = self.water_pixmap.scaled(self.size[0], self.size[1])
        self.cow_pixmap = QPixmap("../assets/textures/cow.png")
        self.cow_pixmap = self.cow_pixmap.scaled(self.size[0], self.size[1])
        self.human_pixmap = QPixmap("../assets/textures/human.png")
        self.human_pixmap = self.human_pixmap.scaled(self.size[0], self.size[1])
        self.plant_pixmap = QPixmap("../assets/textures/plant.png")
        self.plant_pixmap = self.plant_pixmap.scaled(self.size[0], self.size[1])
        self.grid_size = grid_size
        self.pixmap_items = [[[None, None] for _ in range(grid_size[0])] for _ in range(grid_size[1])]

        start_time = time.time()
        self.draw_grid2(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")
        self.scale(0.002, 0.002)

    def draw_grid(self, grid):
        for i, line in enumerate(grid):
            for j, col in enumerate(line):
                for k, entities in enumerate(col):
                    pixmap_item = None
                    match entities:
                        case "L":
                            pixmap_item = QGraphicsPixmapItem(self.land_pixmap)
                        case "W":
                            pixmap_item = QGraphicsPixmapItem(self.water_pixmap)
                        case "H":
                            pixmap_item = QGraphicsPixmapItem(self.human_pixmap)
                        case "C":
                            pixmap_item = QGraphicsPixmapItem(self.cow_pixmap)
                        case "P":
                            pixmap_item = QGraphicsPixmapItem(self.plant_pixmap)

                    pixmap_item.setPos(j * self.size[0], i * self.size[1])
                    self.pixmap_items[i][j][k] = pixmap_item
                    self.scene.addItem(pixmap_item)

    def draw_grid2(self,grid):
        for i, line in enumerate(grid):
            for j, entities in enumerate(line):
                pixmap_item = None
                match entities:
                    case Land():
                        pixmap_item = QGraphicsPixmapItem(self.land_pixmap)
                    case Water():
                        pixmap_item = QGraphicsPixmapItem(self.water_pixmap)

                pixmap_item.setPos(j * self.size[0], i * self.size[1])
                self.pixmap_items[i][j][0] = pixmap_item
                self.scene.addItem(pixmap_item)

    def wheelEvent(self, event):
        # Récupérer le facteur de zoom actuel
        zoom_out = event.angleDelta().y() < 0
        zoom_factor = 1.1 if zoom_out else 0.9

        # Appliquer le zoom
        self.zoom_factor *= zoom_factor
        self.scale(zoom_factor, zoom_factor)