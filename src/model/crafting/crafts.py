from typing import Dict, override

from src.constants import CRAFT_PARAMETERS, ITEMS_TEXTURE_FOLDER_PATH
from src.model.crafting.loots import Loot
from src.model.drawable import ParametrizedDrawable


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
    def _getParameters(cls) -> dict:
        return CRAFT_PARAMETERS

    @classmethod
    @override
    def _getFilePathPrefix(cls) -> str:
        return ITEMS_TEXTURE_FOLDER_PATH

    @classmethod
    def getBlueprint(cls) -> float:
        return cls._getParameter("blueprint")


class FishingRod:
    ...
