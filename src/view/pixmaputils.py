from abc import ABC

from PyQt6.QtGui import QPixmap, QColor, QImage

from parameters import ViewParameters


class PixmapUtils(ABC):

    _pixmapFromPath = {}
    _pixmapFromRGB = {}

    @classmethod
    def getPixmapFromPath(cls, path: str) -> QPixmap:
        if path not in cls._pixmapFromPath:
            pixmap = QPixmap(path)
            pixmap = pixmap.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
            cls._pixmapFromPath[path] = pixmap

        return cls._pixmapFromPath[path]

    @classmethod
    def getPixmapFromRGBHex(cls, rgbHex: str) -> QPixmap:
        if rgbHex not in cls._pixmapFromRGB:
            im = QImage(1, 1, QImage.Format.Format_RGB32)
            im.setPixel(0, 0, QColor(rgbHex).rgb())
            pixmap = QPixmap(im)
            pixmap = pixmap.scaled(ViewParameters.TEXTURE_SIZE, ViewParameters.TEXTURE_SIZE)
            cls._pixmapFromRGB[rgbHex] = pixmap

        return cls._pixmapFromRGB[rgbHex]