from parameters.genericparameters import Parameters
from abc import ABC
from overrides import override


class EntityParameters(Parameters, ABC):

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
