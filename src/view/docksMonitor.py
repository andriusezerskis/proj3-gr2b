from typing import TypeVar

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QFrame, QLabel

from controller.entityInfoController import EntityInfoController
from controller.playerDockController import PlayerDockController
from view.monitor import MonitorWindow, GraphWindow
from view.scrollArea import ScrollArea

from parameters import ViewParameters


class Observer:
    def updateClosure(self):
        ...


class CustomQDock(QDockWidget):
    def __init__(self, mainWindowController, mainWindow, observer):
        super().__init__("", mainWindow)
        self.mainWindowController = mainWindowController
        self.dockLayout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.dockLayout)
        self.setWidget(container)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.observer = observer

        #self.titleBarFrame = QFrame()
        #self.setTitleBarWidget(self.titleBarFrame)

        # Appliquer le style CSS à la barre de titre
        #self.titleBarFrame.setStyleSheet("""
        #            QFrame {
        #                background-color: #2c3e50; /* Couleur de fond de la barre de titre */
        #                color: white; /* Couleur du texte de la barre de titre */
        #                border: none; /* Supprimer la bordure */
        #            }
        #        """)
        #self.titleLabel = QLabel("title")
        #layout = QVBoxLayout(self.titleBarFrame)
        #layout.addWidget(self.titleLabel)
        #self.titleLabel.setFixedHeight(30)
        #layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(ViewParameters.DOCK_BG)


    def updateContent(self, j):
        ...

    def updateController(self):
        ...

    def close(self):
        super().close()
        #print("closed")
        self.mainWindowController.hide_button()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        super().closeEvent(event)
        self.observer.updateClosure()
        self.mainWindowController.closeDockEvent()
        #print("closed by me")


class MonitoringDock(CustomQDock):
    def __init__(self, mainWindowController, mainWindow, observer):
        super().__init__(mainWindowController, mainWindow, observer)

        mainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        container1 = QWidget()
        container2 = QWidget()
        container3 = QWidget()
        self.dockLayout.addWidget(container1)
        self.dockLayout.addWidget(container3)
        self.dockLayout.addWidget(container2)

        self.monitor = MonitorWindow(self, container1)
        self.graph = GraphWindow(self, container3)
        self.entityController = EntityInfoController(self, container2)

    def updateContent(self, j):
        self.graph.updatePlot(j.getCount(), j)

    def updateController(self):
        self.entityController.update()


class PlayerDock(CustomQDock):
    def __init__(self, mainWindowController, mainWindow, observer):
        super().__init__(mainWindowController, mainWindow, observer)

        mainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        container1 = QWidget()
        container2 = QWidget()
        self.dockLayout.addWidget(container1)
        self.dockLayout.addWidget(container2)
        self.playerController = PlayerDockController(self, container1)
        self.scrollArea = ScrollArea(container2)


    def updateContent(self, j):
        return

    def updateController(self):
        return


class DocksMonitor(Observer):
    def __init__(self, mainWindowController, mainWindow):
        self.monitoringDock = MonitoringDock(mainWindowController, mainWindow, self)
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
