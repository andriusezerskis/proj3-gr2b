from parameters.genericparameters import Parameters
from abc import ABC
from overrides import override


class EntityParameters(Parameters, ABC):

    NIGHT_MODE_START: int = None
    MIDDLE_OF_THE_NIGHT: int = None
    NIGHT_MODE_FINISH: int = None
    SUNSET_MODE_START: int = None
    MAX_TILE_FILTER_OPACITY: float = None
    NIGHT_MODE_COLOR: str = None
    SUNSET_MODE_COLOR: str = None
    HIGHTLIGHTED_TILE_TEXTURE_PATH: str = None
    FIRE_TEXTURE_PATH: str = None
    ICE_TEXTURE_PATH: str = None
    CLICKED_BUTTON_STYLESHEET: str = None
    NOT_CLICKED_BUTTON_STYLESHEET: str = None
    TIME_FORMAT: str = None
    GRID_STYLESHEET: str = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "view_parameters.json"
