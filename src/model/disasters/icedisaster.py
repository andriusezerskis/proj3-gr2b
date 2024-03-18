from model.disasters.disaster import Disaster
from parameters import ViewParameters


class IceDisaster(Disaster):

    @classmethod
    def getMaxTemperatureDifference(cls):
        return -20

    @classmethod
    def getMaxDamage(cls):
        return 10

    @classmethod
    def getDuration(cls):
        return 20

    @classmethod
    def getTexturePath(cls):
        return ViewParameters.ICE_TEXTURE_PATH

    def __init__(self, strength: float):
        super().__init__(strength)
