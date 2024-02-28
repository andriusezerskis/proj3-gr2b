from parameters.genericparameters import Parameters
from abc import ABC
from overrides import override


class EntityParameters(Parameters, ABC):

    HUNGRY_THRESHOLD: int = None
    MAX_AGE: int = None
    MAX_HUNGER: int = None
    REPRODUCTION_COOLDOWN: int = None
    REPRODUCTION_MAX_HUNGER: int = None
    REPRODUCTION_MIN_AGE: int = None
    PLANT_REPRODUCTION_PROBABILITY: float = None
    PLANT_ADJACENT_PEERS_AUTO_DEATH_THRESHOLD: int = None
    PLANT_PROBABILITY_DEATH_IF_TOO_MUCH_NEIGHBOURS: float = None

    @classmethod
    @override
    def getFileName(cls) -> str:
        return "entity_parameters.json"
