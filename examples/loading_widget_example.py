import sys

from qtpy.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

from widgets.loading_widget import LoadingWidget


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        button = QPushButton(f"Click to load forever...")
        button.setMaximumWidth(300)
        button.clicked.connect(lambda: LoadingWidget(self).show())

        layout.addWidget(button)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setMinimumSize(500, 500)
    main.show()
    sys.exit(app.exec_())
