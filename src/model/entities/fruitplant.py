from model.entities.plant import Plant
from utils import Point
from overrides import override
from random import choice


class FruitPlant(Plant):

    def __init__(self, pos: Point):
        super().__init__(pos)
        self._fruitCooldown = 0
        self._fruitTexturePath = self.pickRandomFruitTexturePath()

    @override
    def evolve(self) -> bool:
        needsToBeUpdated = self._fruitCooldown == 1
        self._fruitCooldown = max(0, self._fruitCooldown - 1)
        superRet = super().evolve()
        return needsToBeUpdated or superRet

    @override
    def canBeEaten(self) -> bool:
        return self._fruitCooldown == 0

    @override
    def getEaten(self) -> bool:
        self._fruitCooldown = self.getFruitCooldown()
        return False

    @classmethod
    def getFruitCooldown(cls) -> int:
        return cls._getParameter("fruit_cooldown")

    @classmethod
    def pickRandomFruitTexturePath(cls) -> str:
        return cls._constructFullTexturePath(choice(cls._getParameter("fruit_texture_path")))

    @override
    def getTexturePath(self) -> str:
        if self.canBeEaten():
            return self._fruitTexturePath
        return super().getTexturePath()
