from overrides import override

from model.entities.plant import Plant
from model.terrains.water import Water

from utils import Point

from constants import ALGAE_TEXTURE_PATH


class Algae(Plant):
    count = 0

    @staticmethod
    @override
    def getTexturePath() -> str:
        return ALGAE_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Water}

    def __init__(self, pos: Point):
        super().__init__(pos)
        Algae.count += 1

    def __del__(self):
        super().__del__()
        Algae.count -= 1

    def __str__(self):
        return 'A'
