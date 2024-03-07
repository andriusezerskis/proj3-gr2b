from overrides import override

from parameters import CraftParameters
from model.drawable import ParametrizedDrawable


class Loot(ParametrizedDrawable):
    @classmethod
    @override
    def _getConfigFilePath(cls) -> str:
        return "../config/loots.json"

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return CraftParameters.TEXTURE_FOLDER_PATH


class Wood(Loot):
    ...


class Claw(Loot):
    ...
