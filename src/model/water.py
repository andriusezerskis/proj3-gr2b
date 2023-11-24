from case import Case

class Water(Case):
    def __init__(self, entityList) -> None:
        super().__init__(entityList)
        
    def getPossibleEntities(self):
        return []
    
    def get_type(self):
        return "water"