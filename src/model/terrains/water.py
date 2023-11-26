from overrides import override
from case import Case
from entities.fish import Fish
from entities.plankton import Plankton
from entities.entity import Entity

class Water(Case):
    def __init__(self, entity) -> None:
        super().__init__(entity)
        
    @override    
    def getPossibleEntities(self):
        return {Fish, Plankton} # returns a set so that we can check 
    
    def getType(self):
        return "water"