from abc import abstractmethod
from typing import Tuple

from qtpy.QtCore import QEvent, QRect, Qt
from qtpy.QtGui import QColor, QPainter, QPalette
from qtpy.QtWidgets import QPushButton, QWidget


class OverlayWidget(QWidget):
    def __init__(
        self,
        parent: QWidget,
        overlay_width: int,
        overlay_height: int,
        add_close_button: bool,
    ):
        super().__init__(parent)

        self._overlay_width = overlay_width
        self._overlay_height = overlay_height

        self._TRANSPARENT_COLOR = QColor(0, 0, 0, 0)
        self._WINDOW_BACKGROUND_COLOR = QColor(25, 25, 25, 125)
        self._OVERLAY_BACKGROUND_COLOR = self.palette().color(QPalette.Base)

        parent.installEventFilter(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        if add_close_button:
            self._add_close_button()

        self._resize_to_parent()

    def _add_close_button(self):
        self._close_button = QPushButton(self)
        self._close_button.setText("x")
        self._close_button.setFixedSize(30, 30)

        font = self._close_button.font()
        font.setPixelSize(15)
        self._close_button.setFont(font)

        self._close_button.clicked.connect(lambda: self.close())

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Resize:
            self._resize_to_parent()

        return super().eventFilter(obj, event)

    def _resize_to_parent(self):
        self.move(0, 0)
        self.resize(self.parent().width(), self.parent().height())

        overlay_corner_width, overlay_corner_height = self._get_overlay_corner()
        self._close_button.move(
            overlay_corner_width + self._overlay_width - self._close_button.width(),
            overlay_corner_height,
        )

    def _get_window_size(self) -> Tuple[int, int]:
        size = self.size()
        return size.width(), size.height()

    def _get_overlay_corner(self) -> Tuple[int, int]:
        width, height = self._get_window_size()
        overlay_corner_width = int(width / 2 - self._overlay_width / 2)
        overlay_corner_height = int(height / 2 - self._overlay_height / 2)
        return overlay_corner_width, overlay_corner_height

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self._TRANSPARENT_COLOR)
        painter.setBrush(self._WINDOW_BACKGROUND_COLOR)
        width, height = self._get_window_size()
        painter.drawRect(0, 0, width, height)

        painter.setPen(self._TRANSPARENT_COLOR)
        painter.setBrush(self._OVERLAY_BACKGROUND_COLOR)
        rounding_radius = 5
        overlay_rectangle = QRect(
            *self._get_overlay_corner(), self._overlay_width, self._overlay_height
        )
        painter.drawRoundedRect(overlay_rectangle, rounding_radius, rounding_radius)

        self._add_content_to_overlay(painter, overlay_rectangle)

        painter.end()

    @abstractmethod
    def _add_content_to_overlay(self, painter: QPainter, overlay_rectangle: QRect):
        pass
