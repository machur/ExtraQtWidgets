from qtpy.QtCore import QRect, Qt
from qtpy.QtGui import QColor, QPainter
from qtpy.QtWidgets import QWidget

from widgets.overlay_widget import OverlayWidget


class TextOverlayWidget(OverlayWidget):
    def __init__(
        self,
        parent: QWidget,
        text: str,
        overlay_width: int = 300,
        overlay_height: int = 150,
    ):
        super().__init__(parent, overlay_width, overlay_height, add_close_button=True)
        self._text = text

    def _add_content_to_overlay(self, painter: QPainter, overlay_rectangle: QRect):
        font = self.font()
        font.setPixelSize(20)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(overlay_rectangle, Qt.AlignCenter, self._text)
