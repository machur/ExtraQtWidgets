from abc import abstractmethod
from typing import Tuple

from qtpy.QtCore import QEvent, QRect, Qt
from qtpy.QtGui import QColor, QPainter, QPalette
from qtpy.QtWidgets import QPushButton, QWidget

TRANSPARENT_COLOR = QColor(0, 0, 0, 0)
WINDOW_BACKGROUND_COLOR = QColor(200, 200, 200, 125)


class OverlayWidget(QWidget):
    def __init__(
        self,
        parent: QWidget,
        overlay_width: int,
        overlay_height: int,
        add_close_button: bool,
        window_background_color: QColor = WINDOW_BACKGROUND_COLOR,
        overlay_background_color: QColor = None,
    ):
        super().__init__(parent)

        self._overlay_width = overlay_width
        self._overlay_height = overlay_height

        self._window_background_color = window_background_color

        if not overlay_background_color:
            overlay_background_color = self.palette().color(QPalette.Base)
        self._overlay_background_color = overlay_background_color

        parent.installEventFilter(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._close_button = self._create_close_button() if add_close_button else None

    def showEvent(self, event):
        self._resize_to_parent()

    def _create_close_button(self):
        close_button = QPushButton(self)
        close_button.setText("x")
        close_button.setFixedSize(30, 30)

        font = close_button.font()
        font.setPixelSize(15)
        close_button.setFont(font)

        close_button.clicked.connect(lambda: self.close())
        return close_button

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Resize:
            self._resize_to_parent()

        return super().eventFilter(obj, event)

    def _resize_to_parent(self):
        self.move(0, 0)
        self.resize(self.parent().width(), self.parent().height())

        overlay_corner_width, overlay_corner_height = self._get_overlay_corner()
        if self._close_button:
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
        painter.setPen(TRANSPARENT_COLOR)
        painter.setBrush(self._window_background_color)
        width, height = self._get_window_size()
        painter.drawRect(0, 0, width, height)

        painter.setPen(TRANSPARENT_COLOR)
        painter.setBrush(self._overlay_background_color)
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
