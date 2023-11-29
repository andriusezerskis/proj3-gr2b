
from model.gridgenerator import GridGenerator


class Grid:
    def __init__(self, size: tuple) -> None:
        self.tiles = []
        self.size = size

    def initialize(self):
        """Random initialization of the grid with perlin noise"""
        self.tiles = GridGenerator(self.size[0], self.size[1]).generateGrid()

    def entitiesInAdjacentTile(self, currentTile):
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
        entitiesList = []

        for tile in adjacent_tiles:
            if 0 <= tile[0] < self.size[0] and 0 <= tile[1] < self.size[1]:
                if self.tiles[tile[0]][tile[1]].getEntity():
                    entitiesList.append(
                        self.tiles[tile[0]][tile[1]].getEntity())

        return entitiesList


    def moveEntity(self, entity, currentTile, nextTile):
        """Moves an entity from a tile to another"""
        if not self.tiles[nextTile[0]][nextTile[1]].hasEntity():
            self.tiles[nextTile[0]][nextTile[1]].addEntity(entity)
            self.tiles[currentTile[0]][currentTile[1]].removeEntity()