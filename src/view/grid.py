import time
from typing import Tuple

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView


class Window(QMainWindow):
    def __init__(self, grid_size: Tuple[int, int], grid):
        super().__init__()
        self.setWindowTitle('Simulation 2D')
        self.setGeometry(100, 100, 400, 400)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # probably in another window later
        self.land_pixmap = QPixmap("../assets/textures/land2.png")
        self.water_pixmap = QPixmap("../assets/textures/water2.png")
        self.cow_pixmap = QPixmap("../assets/textures/cow2.png")
        self.human_pixmap = QPixmap("../assets/textures/human2.png")
        self.plant_pixmap = QPixmap("../assets/textures/plant2.png")
        self.grid_size = grid_size
        self.pixmap_items = [[[None, None] for _ in range(grid_size[0])] for _ in range(grid_size[1])]

        start_time = time.time()
        self.draw_grid(grid)
        exec_time = time.time() - start_time
        print(f"drawn in: {exec_time}s")

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

                    pixmap_item.setPos(j * 16, i * 16)
                    self.pixmap_items[i][j][k] = pixmap_item
                    self.scene.addItem(pixmap_item)
