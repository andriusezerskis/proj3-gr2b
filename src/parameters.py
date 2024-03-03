from parameter.genericparameters import GenericParameters
from abc import ABC
from overrides import override


class EntityParameters(GenericParameters, ABC):

    HUNGRY_THRESHOLD: int = None
    MAX_AGE: int = None
    MAX_HUNGER: int = None
    REPRODUCTION_COOLDOWN: int = None
    REPRODUCTION_MAX_HUNGER: int = None
    REPRODUCTION_MIN_AGE: int = None
    PLANT_ADJACENT_PEERS_AUTO_DEATH_THRESHOLD: int = None
    TEXTURE_FOLDER_PATH: str = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "entity_parameters.json"


class TerrainParameters(GenericParameters, ABC):

    # # Climate
    # Temperature difference between winter and summer
    SEASON_TEMPERATURE_DIFFERENCE: int = None
    MAX_TEMPERATURE_DIFFERENCE: int = None  # in degrees
    MAX_RANDOM_TEMPERATURE_DIFFERENCE: int = None  # in degrees
    YEAR_DURATION: int = None  # year duration in timesteps
    AVERAGE_TEMPERATURE: int = None  # in degrees
    # number of timesteps before an update (for performance)
    NB_STEP_BEFORE_UPDATE: int = None

    # the water level will oscillate between WATER_LEVEL and MAX_WATER_LEVEL in a sinusoidal manner
    # WATER_LEVEL < MAX_WATER_LEVEL < SAND_LEVEL
    MAX_WATER_LEVEL: float = None
    DAY_DURATION: int = None

    # # Entity generation
    # the probability that a tile does not contain any entity at generation
    EMPTY_TILE_PROBABILITY_GENERATION: float = None
    TEXTURE_FOLDER_PATH: str = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "terrain_parameters.json"


class ViewParameters(GenericParameters, ABC):

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
    TEXTURE_SIZE: int = None
    STEP_TIME: int = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "view_parameters.json"


class ViewText(GenericParameters, ABC):

    MAIN_WINDOW_TITLE: str = None
    COMMANDS_WINDOW_TITLE: str = None
    MOVE_CAMERA_UP: str = None
    ENTITY_DEAD_MESSAGE: str = None
    ENTITY_NOT_SELECTED: str = None
    CONTROL_PLAYER: str = None
    HEALTH_BAR_TEXT: str = None
    RELEASE_PLAYER: str = None
    AGE_TEXT: str = None
    NAME_TEXT: str = None
    HUNGER_TEXT: str = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "view_text.json"


class CraftParameters(GenericParameters, ABC):

    TEXTURE_FOLDER_PATH: str = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "crafting_parameters.json"
