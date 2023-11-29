from overrides import override
from random import random

from model.entities.plant import Plant

from constants import ALGAE_TEXTURE_PATH


class Algae(Plant):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return ALGAE_TEXTURE_PATH

    def __init__(self):
        super().__init__()
        
    @override
    def reproduce(self) -> None:
        kidsProbability = [(0, 0.1), (1, 0.4), (2, 0.3), (3, 0.2)]
        return random.choices(kidsProbability, weights=[prob for _, prob in kidsProbability])[0]

