from abc import abstractmethod

class Case:
    def __init__(self, entityList: list) -> None:
        self.entities = entityList
        
    def get_entities(self):
        return self.entities
    
    @abstractmethod
    def getPossibleEntities(self):
        pass