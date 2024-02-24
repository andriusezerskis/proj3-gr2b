from typing import override

from constants import LOOT_PARAMETERS, ITEMS_TEXTURE_FOLDER_PATH
from model.drawable import ParametrizedDrawable


class Loot(ParametrizedDrawable):
    @classmethod
    @override
    def _getParameters(cls) -> dict:
        return LOOT_PARAMETERS

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return ITEMS_TEXTURE_FOLDER_PATH

    @classmethod
    def getDropChance(cls) -> float:
        return cls._getParameter("drop_chance")


class Wood(Loot):
    ...

class Claw(Loot):
    ...

