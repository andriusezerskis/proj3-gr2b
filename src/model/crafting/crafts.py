from typing import Dict, override

from parameters import CraftParameters

from model.crafting.loots import Loot
from model.drawable import ParametrizedDrawable


class Craft(ParametrizedDrawable):
    def __init__(self):
        super().__init__()
        self.blueprint: Dict[Loot, int] = self.getBlueprint()

    def hasEnoughQuantity(self, materials: Dict[Loot, int]):
        for material, quantity in materials.items():
            if self.blueprint.get(material) and self.blueprint.get(material) > quantity:
                return False

    def craft(self, materials: Dict[Loot, int]):
        if not self.hasEnoughQuantity(materials):
            return False
        for material, quantity in self.blueprint:
            materials[material] -= quantity

    @classmethod
    @override
    def _getConfigFilePath(cls) -> str:
        return "../config/crafts.json"

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return CraftParameters.TEXTURE_FOLDER_PATH

    @classmethod
    def getBlueprint(cls) -> Dict[str, int]:
        return cls._getParameter("blueprint")

    @classmethod
    def isValidItemType(cls, itemType: type) -> bool:
        return itemType.__name__ in cls.getBlueprint()


class FishingRod(Craft):
    ...


class Fence(Craft):
    ...
