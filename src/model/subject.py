"""
Project 3: Ecosystem simulation in 2D
Authors: Loïc Blommaert, Hà Uyên Tran, Andrius Ezerskis, Mathieu Vannimmen, Moïra Vanderslagmolen
Date: December 2023
"""


from abc import ABC


class Subject(ABC):
    def __init__(self):
        self.observers = []

    def addObserver(self, observer):
        self.observers.append(observer)

    def notify(self, query=None):
        for observer in self.observers:
            ...