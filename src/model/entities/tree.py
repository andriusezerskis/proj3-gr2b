from model.entities.plant import Plant
from overrides import override
from random import random

from utils import Point

from model.terrains.land import Land


class Tree(Plant):
    count = 0

    def __init__(self, pos: Point):
        super().__init__(pos)
        Tree.count += 1

    def __del__(self):
        super().__del__()
        Tree.count -= 1

    def __str__(self):
        return 'T'

