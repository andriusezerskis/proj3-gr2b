from abc import abstractmethod

class Case:
    def __init__(self, index: tuple, entityList: list) -> None:
        self.index = index
        self.entities = entityList
        
    @abstractmethod
    def step(self):
        pass
    
    @abstractmethod
    def getPossibleEntities(self):
        pass
        
    def getEntities(self):
        return self.entities
    
    def addEntity(self, entity):
        self.entities.append(entity)
        
    def removeEntity(self, entity):
        self.entities.remove(entity)