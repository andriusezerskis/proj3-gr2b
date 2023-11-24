from abc import ABC, abstractmethod


class Entity(ABC):

    def eat(self):
        self.isFed = True

    def __init__(self):
        self.age: int = 0
        self.isFed: bool = False

