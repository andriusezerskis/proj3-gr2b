from PyQt6.QtCore import *


class GridController:
    """Singleton"""
    instance = None

    def __new__(cls, graphical_grid, simulation, rendering_monitor):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls.graphical_grid = graphical_grid
            cls.simulation = simulation
            cls.rendering_monitor = rendering_monitor
            cls.size = [2048, 2048]
        return cls.instance

    @staticmethod
    def getInstance():
        return GridController.instance

    def keyPressEvent(self, event):
        match event.key():
            # camera
            case Qt.Key.Key_Up:
                self.graphical_grid.moveCamera(self.rendering_monitor.up())
            case Qt.Key.Key_Left:
                self.graphical_grid.moveCamera(self.rendering_monitor.left())
            case Qt.Key.Key_Down:
                self.graphical_grid.moveCamera(self.rendering_monitor.down())
            case Qt.Key.Key_Right:
                self.graphical_grid.moveCamera(self.rendering_monitor.right())

            # player
            case Qt.Key.Key_Z:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((-1, 0)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
            case Qt.Key.Key_Q:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, -1)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
            case Qt.Key.Key_S:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((1, 0)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())
            case Qt.Key.Key_D:
                if self.simulation.hasPlayer():
                    pos = self.simulation.getPlayer().getPosition()
                    if self.simulation.getPlayer().move((0, 1)):
                        self.graphical_grid.movePlayer(
                            pos, self.simulation.getPlayer().getPosition())

    def mousePressEvent(self, event):
        # si j'enlève ça ça marche pas jcomprends pas pq mais dcp je le laisse
        print("bruh")
        scene_pos = self.graphical_grid.mapToScene(event.pos())
        tile = self.getClickedTile(scene_pos.x(), scene_pos.y())
        if tile.hasEntity():
            # self.simulation.setPlayerEntity(tile)
            self.graphical_grid.drawEntityInfo(tile.getEntity())

    def getClickedTile(self, x, y):
        """Crash here if not on a pixmap"""
        return self.simulation.getGrid().getTile(int(y // self.size[1]), int(x // self.size[0]))

    def wheelEvent(self, event):
        """zoom_out = event.angleDelta().y() < 0
        zoom_factor = 1.1 if zoom_out else 0.9

        self.zoom_factor *= zoom_factor
        self.scale(zoom_factor, zoom_factor)"""
        return
