from model.noiseGenerator import NoiseGenerator
from model.terrains.tile import Tile
from model.terrains.water import Water
from model.terrains.land import Land
from model.terrains.sand import Sand
from model.terrains.mountain import Mountain
from model.grid import Grid

from utils import Point

from constants import WATER_LEVEL, SAND_LEVEL, LAND_LEVEL, MOUNTAIN_LEVEL


class GridGenerator:

    def __init__(self, size: Point, islandNb: list[int], islandSize: int,
                 thresholds=((Water, WATER_LEVEL), (Sand, SAND_LEVEL), (Land, LAND_LEVEL), (Mountain, MOUNTAIN_LEVEL))):
        """
        :param size: x: width of the map, y: height of the map
        :param island_nb: number of islands in the grid (an array of possible values)
        :param island_size: minimal number of land tiles in an island
        :param thresholds: mapping of height (in [-1;1]) to type of tile
        """
        self.noiseGenerator = None
        self.w = size.x()
        self.h = size.y()
        self.matrix = None
        self.islandNb = islandNb
        self.islandSize = islandSize
        self.thresholds = thresholds
        self.maxAbsHeight = 0

    def _getTile(self, x: int, y: int) -> Tile:
        sample = self.noiseGenerator.sample2D(
            x/self.w, y/self.h) / self.maxAbsHeight
        for tileType, threshold in self.thresholds:

            if sample <= threshold:
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
                    if len(islands) >= max(self.islandNb):
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

    def getNormalizationBorns(self) -> None:
        self.maxAbsHeight = 0
        for y in range(self.h):
            for x in range(self.w):
                sample = self.noiseGenerator.sample2D(x/self.w, y/self.h)
                self.maxAbsHeight = max(self.maxAbsHeight, abs(sample))

    def generateGrid(self) -> Grid:
        islands = []
        size_ok = False
        print("Generating terrain...")
        while len(islands) not in self.islandNb or not size_ok:
            self.noiseGenerator = NoiseGenerator()
            self.noiseGenerator.addNoise(2, 1)
            self.noiseGenerator.addNoise(4, 0.5)
            self.getNormalizationBorns()
            self.matrix = self._generateMatrix()
            islands = self.getIslands()
            size_ok = True
            for island in islands:
                if len(island) < self.islandSize:
                    size_ok = False
                    break

        grid = Grid(Point(self.w, self.h))
        grid.initialize(self.matrix, islands)
        print("Terrain generated")
        return grid
