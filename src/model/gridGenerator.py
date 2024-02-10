from model.noiseGenerator import NoiseGenerator
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land
from model.terrains.sand import Sand

from utils import Point

from constants import WATER_LEVEL, SAND_LEVEL, LAND_LEVEL


class GridGenerator:

    def __init__(self, w: int, h: int, island_nb: list[int], island_size: int,
                 thresholds=((Water, WATER_LEVEL), (Sand, SAND_LEVEL), (Land, LAND_LEVEL))):
        """
        :param w: width of the map in #tiles
        :param h: height of the map in #tiles
        :param island_nb: number of islands in the grid (an array of possible values)
        :param island_size: minimal number of land tiles in an island
        :param thresholds: mapping of height (in [-1;1]) to type of tile
        """
        self.noiseGenerator = None
        self.w = w
        self.h = h
        self.matrix = None
        self.island_nb = island_nb
        self.island_size = island_size
        self.thresholds = thresholds

    def _getTile(self, x: int, y: int) -> Tile:
        sample = self.noiseGenerator.sample2D(x/self.w, y/self.h)
        for tileType, threshold in self.thresholds:

            if sample < threshold:
                return tileType(Point(x, y), sample)

    def _generateMatrix(self) -> list[list[Tile]]:
        return [[self._getTile(x, y) for x in range(self.w)] for y in range(self.h)]

    def getIslands(self) -> list[set[Tile]]:
        islands = []
        visited = set()
        for y, row in enumerate(self.matrix):
            for x, tile in enumerate(row):
                if type(tile) is not Water and tile not in visited:

                    # new island found
                    if len(islands) >= max(self.island_nb):
                        # no need to look further, we've found too many islands
                        return []

                    visited.add(tile)
                    island = set()

                    self._getIsland(x, y, island, visited)
                    islands.append(island)

                else:
                    visited.add(tile)

        return islands

    def _getIsland(self, x: int, y: int, island: set[Tile], visited: set[Tile]) -> None:
        stack = [(x, y)]
        while len(stack) > 0:
            x, y = stack.pop()
            island.add(self.matrix[y][x])
            for newx, newy in [(x + offsetx, y + offsety) for offsetx in [-1, 0, 1] for offsety in [-1, 0, 1]]:
                if (0 <= newx < self.w and 0 <= newy < self.h and self.matrix[newy][newx] not in visited and
                        type(self.matrix[newy][newx]) is not Water):
                    visited.add(self.matrix[newy][newx])
                    stack.append((newx, newy))

    def generateGrid(self) -> tuple[list[list[Tile]], set[Tile]]:
        islands = set()
        size_ok = False
        print("Generating terrain...")
        while len(islands) not in self.island_nb or not size_ok:
            self.noiseGenerator = NoiseGenerator()
            self.noiseGenerator.addNoise(2, 1)
            self.noiseGenerator.addNoise(4, 0.5)
            self.matrix = self._generateMatrix()
            islands = self.getIslands()
            size_ok = True
            for island in islands:
                if len(island) < self.island_size:
                    size_ok = False
                    break
        print("Terrain generated")
        return self.matrix, islands
