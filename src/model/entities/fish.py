from utils import Point

from model.entities.animal import Animal


class Fish(Animal):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Fish.count += 1

    def __del__(self):
        super().__del__()
        Fish.count -= 1

    def __str__(self):
        return 'F'
