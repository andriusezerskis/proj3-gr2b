from model.entities.plant import Plant
from utils import Point


class Algae(Plant):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Algae.count += 1

    def __del__(self):
        super().__del__()
        Algae.count -= 1

    def __str__(self):
        return 'A'
