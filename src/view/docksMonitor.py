from typing import TypeVar, Type
from model.entities.entity import Entity

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QFrame, QLabel

from controller.entityInfoController import EntityInfoController
from controller.mainWindowController import MainWindowController
from controller.playerDockController import PlayerDockController
from view.monitor import MonitorWindow, GraphWindow
from view.scrollArea import ScrollArea

from parameters import ViewParameters


class Observer:
    def updateClosure(self):
        ...


class CustomQDock(QDockWidget):
    def __init__(self, mainWindowController: MainWindowController, mainWindow: "Window", observer):
        super().__init__("", mainWindow)
        self.mainWindowController = mainWindowController
        self.dockLayout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.dockLayout)
        self.setWidget(container)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.observer = observer

    def updateContent(self, j):
        ...

    def updateController(self):
        ...

    def close(self):
        super().close()
        self.mainWindowController.hide_button()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        super().closeEvent(event)
        self.observer.updateClosure()
        self.mainWindowController.closeDockEvent()


class MonitoringDock(CustomQDock):
    def __init__(self, mainWindowController: MainWindowController, mainWindow: "Window", observer):
        super().__init__(mainWindowController, mainWindow, observer)

        mainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        container1 = QWidget()
        container2 = QWidget()
        container3 = QWidget()
        self.dockLayout.addWidget(container1)
        self.dockLayout.addWidget(container3)
        self.dockLayout.addWidget(container2)
        container1.setObjectName("Dock")
        container2.setObjectName("Dock")
        container3.setObjectName("Dock")

        self.monitor = MonitorWindow(container1)
        self.graph = GraphWindow(container3)
        self.entityController = EntityInfoController(container2)

    def updateContent(self, entityType: Type[Entity]):
        self.graph.updatePlot(entityType.getCount(), entityType)

    def redrawPlot(self) -> None:
        self.graph.drawPlot()

    def addNewStep(self) -> None:
        self.graph.addNewStep()

    def updateController(self):
        self.entityController.update()


class PlayerDock(CustomQDock):
    def __init__(self, mainWindowController: MainWindowController, mainWindow: "Window", observer):
        super().__init__(mainWindowController, mainWindow, observer)

        mainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        container1 = QWidget()
        container2 = QWidget()
        self.dockLayout.addWidget(container1)
        self.dockLayout.addWidget(container2)
        self.playerController = PlayerDockController(container2)
        self.scrollArea = ScrollArea(container1)
        
    def addNewStep(self) -> None:
        ...
        
    def redrawPlot(self) -> None:
        ...


class DocksMonitor(Observer):
    def __init__(self, mainWindowController: MainWindowController, mainWindow: "Window"):
        self.monitoringDock = MonitoringDock(
            mainWindowController, mainWindow, self)
        self.playerDock = PlayerDock(mainWindowController, mainWindow, self)
        self.docks = [self.monitoringDock, self.playerDock]

        self.currentDock = 0
        self.docks[1-self.currentDock].close()
        self.displayed = True

    def changeCurrentDock(self):
        self.docks[self.currentDock].close()
        self.currentDock = 1 - self.currentDock
        self.docks[self.currentDock].show()

    def closeDock(self):
        self.displayed = False
        self.docks[self.currentDock].close()

    def openDock(self):
        self.displayed = True
        self.docks[self.currentDock].show()

    def getCurrentDock(self):
        return self.docks[self.currentDock]

    def isMonitoringDock(self):
        return self.currentDock == 0

    def isPlayerDock(self):
        return self.currentDock == 1

    def isDisplayed(self):
        return self.displayed

    def updateClosure(self):
        self.displayed = False
