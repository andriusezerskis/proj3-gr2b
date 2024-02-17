from utils import Point
from model.entities.animal import Animal


class Crab(Animal):
    count = 0
    
    def __init__(self, pos: Point):
        super().__init__(pos)
        Crab.count += 1

    def __del__(self):
        super().__del__()
        Crab.count -= 1
