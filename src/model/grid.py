from case import Case

class Grid:
    def __init__(self, size: tuple) -> None:
        self.cases = []
        self.size = size
        
    def initialize(self):
        """Probably useless, need random initialization"""
        for line in range(self.size[0]):
            self.cases.append([])
            for col in range(self.size[1]):
                self.cases[line].append(Case([]))
                
        # add entities randomly TODO
                
    def entityInAdjacentCase(self, entity, currentCase):
        """Checks if, given a current case, there's an entity in an adjacent case to eventually interact with"""
        adjacent_cases = [
            (currentCase[0] - 1, currentCase[1]),  # up
            (currentCase[0] + 1, currentCase[1]),  # down
            (currentCase[0], currentCase[1] - 1),  # left
            (currentCase[0], currentCase[1] + 1),  # right
            (currentCase[0] - 1, currentCase[1] - 1),  # upper left
            (currentCase[0] - 1, currentCase[1] + 1),  # upper right
            (currentCase[0] + 1, currentCase[1] - 1),  # lower left
            (currentCase[0] + 1, currentCase[1] + 1)  # lower right
        ]
        
        for case in adjacent_cases:
            if 0 <= case[0] < self.size[0] and 0 <= case[1] < self.size[1]:
                if entity.id == self.cases[case[0]][case[1]].getEntity().id:
                    return True
        return False
