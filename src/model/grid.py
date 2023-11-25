from case import Case

class Grid:
    def __init__(self, size: tuple) -> None:
        self.cases = []
        self.size = size
        
    def initialize(self):
        for line in range(self.size[0]):
            self.cases.append([])
            for col in range(self.size[1]):
                self.cases[line].append(Case([]))
                
    def step(self):
        for row in self.cases:
            for case in row:
                # if two entities are on the same case, they interact
                # get both entities
                # apply relation
                ...