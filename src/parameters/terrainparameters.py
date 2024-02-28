from parameters.genericparameters import Parameters
from abc import ABC
from overrides import override


class EntityParameters(Parameters, ABC):

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

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "terrain_parameters.json"
