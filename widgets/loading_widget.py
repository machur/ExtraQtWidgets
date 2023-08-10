import math
import os

from qtpy.QtCore import QRect, Qt, QTimer
from qtpy.QtGui import QImage, QPainter, QTransform
from qtpy.QtWidgets import QWidget

from widgets.overlay_widget import OverlayWidget, TRANSPARENT_COLOR


class LoadingWidget(OverlayWidget):
    def __init__(self, parent: QWidget):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        loading_icon_path = os.path.join(current_dir, "..", "icons", "loading.png")
        self._icon = QImage(loading_icon_path).scaled(100, 100, Qt.KeepAspectRatio)

        size = self._icon.size()
        overlay_size = math.sqrt(size.width() ^ 2 + size.height() ^ 2)

        super().__init__(parent, overlay_size, overlay_size, add_close_button=False)

        self._icon_to_plot = self._icon
        self._rotation = QTransform()

        rotation_timer = QTimer(self)
        rotation_timer.timeout.connect(lambda: self._rotate_icon())
        rotation_timer.start(20)

    def _rotate_icon(self, angle: float = 5.0):
        self._icon_to_plot = self._icon.transformed(
            self._rotation, Qt.SmoothTransformation
        )
        self._rotation = self._rotation.rotate(angle)
        self.repaint()

    def _add_content_to_overlay(self, painter: QPainter, overlay_rectangle: QRect):
        font = self.font()
        font.setPixelSize(20)
        painter.setFont(font)
        painter.setPen(TRANSPARENT_COLOR)

        center = overlay_rectangle.center()
        x = center.x()
        y = center.y()

        size = self._icon_to_plot.size()
        icon_width = size.width()
        icon_height = size.height()

        icon_rectangle = QRect(
            x - icon_width / 2, y - icon_height / 2, icon_width, icon_height
        )

        painter.drawImage(icon_rectangle, self._icon_to_plot)
