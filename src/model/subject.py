from abc import ABC


class Subject(ABC):
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        self.observers.append(observer)

    def notify(self, query=None):
        for observer in self.observers:
            observer.pingUpdate(query)