import random
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        random.seed(3)
        self.setWindowTitle('Simulation 2D')
        self.setGeometry(100, 100, 400, 400)
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 1, 0, 1)
        self.drawGrid([])
        self.wid.setLayout(self.layout)
        self.wid.show()
        self.show()

    def drawGrid(self, grid):  # from the model
        grid = [[random.choice(["LH", "LC", "LP", "L", "W"]) for _ in range(20)] for _ in range(20)]

        for i, line in enumerate(grid):
            for j, col in enumerate(line):
                for entities in col:
                    pixmap = None
                    match entities:
                        case "L":
                            pixmap = QPixmap("../../assets/textures/land.png")
                        case "W":
                            pixmap = QPixmap("../../assets/textures/water.png")
                        case "H":
                            pixmap = QPixmap("../../assets/textures/human.png")
                        case "C":
                            pixmap = QPixmap("../../assets/textures/cow.png")
                        case "P":
                            pixmap = QPixmap("../../assets/textures/plant.png")
                    # Création du label pour afficher l'image dans la cellule de la grille
                    pixmap = pixmap.scaled(100, 100)
                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setScaledContents(True)  # Redimensionner l'image pour s'adapter au label
                    self.layout.addWidget(label, i, j)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())