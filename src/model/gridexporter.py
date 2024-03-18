import time
from abc import ABC

from model.entities.entity import Entity
from time import time_ns
from model.grid import Grid
from utils import Point


class GridExporter(ABC):
    @staticmethod
    def exportToMap(grid: Grid, folderPath: str = "../assets/grids", precision: int = 4) -> None:
        res = ""
        res += f"{grid.getSize().y()}\n{grid.getSize().x()}\n"

        res += "################\n"

        entities = ""

        for y in range(grid.getSize().y()):
            for x in range(grid.getSize().x()):
                tile = grid.getTile(Point(x, y))
                res += f"{round(tile.getHeight(), precision)} "

                entity = tile.getEntity()

                if not entity or not isinstance(entity, Entity):
                    symbol = "-"
                else:
                    symbol = entity.getSymbol()

                entities += f"{symbol} "
            res += "\n"
            entities += "\n"

        res += "################\n"
        res += entities

        with open(f"{folderPath}/map_{time_ns()}.map", "w") as f:
            f.write(res)
