import threading


class ConditionStorage:
    exist = False

    def __init__(self, exist=False):
        assert ConditionStorage.exist or exist
        self.mapLoadingCondition = threading.Condition()
        self.computingCondition = threading.Condition()

    def getMapLoadingCondition(self):
        return self.mapLoadingCondition

    def getComputingConditon(self):
        return self.computingCondition

    def __del__(self):
        print("anormal")