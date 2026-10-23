import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
)


class GPIOTeleopWidget(QGroupBox):
    """Control the robot's GPIO output."""

    gpio_command = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__("GPIO Control", parent)

        self.toggle_button = QPushButton("GPIO Off")
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggled.connect(self._on_toggled)

        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)
        self.setLayout(layout)

    def _on_toggled(self, enabled: bool):
        self.toggle_button.setText("GPIO On" if enabled else "GPIO Off")
        self.gpio_command.emit(enabled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = GPIOTeleopWidget()
    widget.show()
    sys.exit(app.exec())