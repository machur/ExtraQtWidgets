import sys

from qtpy.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

from widgets.text_overlay_widget import TextOverlayWidget


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._create_button_widget("Hello!", 200, False))
        layout.addWidget(self._create_button_widget("Hola!", 200, False))
        layout.addWidget(
            self._create_button_widget("Hi in the whole window!", 400, True)
        )
        self.setLayout(layout)

    def _create_button_widget(
        self, text: str, overlay_width: int, show_on_full_window: bool
    ):
        widget = QWidget()
        widget.setMinimumWidth(300)
        widget.setMinimumHeight(500)

        button = QPushButton(f"Say '{text}'")
        overlay_parent = self if show_on_full_window else widget
        button.clicked.connect(
            lambda: TextOverlayWidget(overlay_parent, text, overlay_width).show()
        )

        layout = QHBoxLayout()
        layout.addWidget(button)
        widget.setLayout(layout)

        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
