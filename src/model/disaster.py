from enum import Enum


class Disaster(str, Enum):
    FIRE_TEXT = "Explosion",
    ICE_TEXT = "Froid glacial"
    INVASION_TEXT = "Invasion de:"
