from model.entities.animal import Animal
from utils import Point


class Human(Animal):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Human.count += 1

    def __del__(self):
        super().__del__()
        Human.count -= 1

    def __str__(self):
        return 'H'
  