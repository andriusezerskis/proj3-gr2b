from model.entities.entity import Entity
from utils import getTerminalSubclassesOfClass


def getFrenchToEnglishTranslation(frenchEntity: str) -> str:
    for entityType in getTerminalSubclassesOfClass(Entity):
        if entityType.getFrenchName() == frenchEntity:
            return entityType.__name__
