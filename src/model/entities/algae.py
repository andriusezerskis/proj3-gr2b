from overrides import override

from model.entities.plant import Plant
from model.terrains.water import Water

from constants import ALGAE_TEXTURE_PATH


class Algae(Plant):

    def __init__(self):
        super().__init__()

    @staticmethod
    @override
    def getTexturePath() -> str:
        return ALGAE_TEXTURE_PATH

    @staticmethod
    @override
    def getValidTiles() -> set[type]:
        return {Water}

    @override
    def reproduce(self) -> None:
        # kidsProbability = [(0, 0.1), (1, 0.4), (2, 0.3), (3, 0.2)]
        # return random.choices(kidsProbability, weights=[prob for _, prob in kidsProbability])[0]
        return True

    def __str__(self):
        return 'A'
