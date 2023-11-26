from overrides import override

from plant import Plant

from constants import ALGAE_TEXTURE_PATH


class Algae(Plant):

    @staticmethod
    @override
    def getTexturePath() -> str:
        return ALGAE_TEXTURE_PATH

    def __init__(self):
        super().__init__()
