from overrides import override
from model.case import Case
from model.entities.fish import Fish
from model.entities.plankton import Plankton
from model.entities.entity import Entity

class Water(Case):
    def __init__(self, entity: Entity=None) -> None:
        super().__init__(entity)
        
    @override    
    def getPossibleEntities(self):
        return {Fish, Plankton} # returns a set so that we can check 
    
    def getType(self):
        return "water"