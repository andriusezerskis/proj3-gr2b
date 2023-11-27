
from gridgenerator import GridGenerator


class Grid:
    def __init__(self, size: tuple) -> None:
        self.tiles = []
        self.size = size
        
    def initialize(self):
        """Random initialization of the grid with perlin noise"""
        self.tiles = GridGenerator(self.size[0], self.size[1]).generateGrid()
                
    def entityInAdjacentCase(self, entity, currentTile):
        """Checks if, given a current tile, there's an entity in an adjacent case to eventually interact with"""
        adjacent_tiles = [
            (currentTile[0] - 1, currentTile[1]),  # up
            (currentTile[0] + 1, currentTile[1]),  # down
            (currentTile[0], currentTile[1] - 1),  # left
            (currentTile[0], currentTile[1] + 1),  # right
            (currentTile[0] - 1, currentTile[1] - 1),  # upper left
            (currentTile[0] - 1, currentTile[1] + 1),  # upper right
            (currentTile[0] + 1, currentTile[1] - 1),  # lower left
            (currentTile[0] + 1, currentTile[1] + 1)  # lower right
        ]
        
        for tile in adjacent_tiles:
            if 0 <= tile[0] < self.size[0] and 0 <= tile[1] < self.size[1]:
                if entity.id == self.tiles[tile[0]][tile[1]].getEntity().id:
                    return True
        return False
