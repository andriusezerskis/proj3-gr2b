from abc import abstractmethod, ABC

from model.entities.entity import Entity

from utils import Point


class Tile(ABC):

    @staticmethod
    @abstractmethod
    def getTexturePath() -> str:
        ...

    def __init__(self, pos: Point, height: float, entity: Entity = None) -> None:
        self.pos = pos
        self.height = height
        self.entity = None
        # we only set the entity if the tile is of a valid type
        if entity and self.__class__ in entity.getValidTiles():
            self.entity = entity
        
    # @abstractmethod
    def step(self):
        pass
        
    def getEntity(self) -> Entity | None:
        return self.entity

    def hasEntity(self) -> bool:
        return self.entity is not None

    def setEntity(self, entity: Entity) -> None:
        self.entity = entity

    def addNewEntity(self, entity: type) -> None:
        """
        Places a new entity in this tile
        :param entity: the type of entity that must be created
        """
        if not self.entity:
            self.entity = entity(self.pos)
        
    def removeEntity(self) -> None:
        if self.entity:
            self.entity = None

    def getPos(self) -> Point:
        return self.pos

    @property
    def index(self) -> tuple[int, int]:
        return self.getIndex()

    def getIndex(self) -> tuple[int, int]:
        return self.pos.y(), self.pos.x()

    @staticmethod
    def copyWithDifferentTypeOf(toCopy: "Tile", type_: type) -> "Tile":
        return type_(toCopy.pos, toCopy.height, toCopy.entity)

    def __repr__(self):
        return f"Tile({self.pos})"

    def __str__(self):
        ...
