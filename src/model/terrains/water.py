from overrides import override
from case import Case
from entities.fish import Fish
from entities.plankton import Plankton

class Water(Case):
    def __init__(self, entityList) -> None:
        super().__init__(entityList)
        
    @override    
    def getPossibleEntities(self):
        return {Fish(), Plankton()} # returns a set so that we can check 
    
    def getType(self):
        return "water"