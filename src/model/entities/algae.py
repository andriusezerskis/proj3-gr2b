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

    @override
    def reproduce(self) -> None:
        # kidsProbability = [(0, 0.1), (1, 0.4), (2, 0.3), (3, 0.2)]
        # return random.choices(kidsProbability, weights=[prob for _, prob in kidsProbability])[0]
        return True

    def __str__(self):
        return 'A'
