import sys

from PyQt6.QtCore import (
  pyqtSignal,
  Qt
)
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QLabel
)
from PyQt6.QtGui import (
    QFont,
    QKeyEvent
)


class GPIOTeleopWidget(QGroupBox):
    """Control the robot's GPIO output."""

    gpio_command = pyqtSignal(bool, bool, int, str)

    STEP_TOP_STEP_FREQUENCY = 1000
    STEP_BOT_STEP_FREQUENCY = 1000
    MIN_STEP_FREQUENCY = 10
    MAX_STEP_FREQUENCY = 7000

    def __init__(self, parent=None):
        super().__init__("GPIO Control", parent)
        self.enabled = False
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        top_motor = QVBoxLayout()
        bot_motor = QHBoxLayout()

        top_step_layout = QHBoxLayout()
        top_step_frequency_layout = QVBoxLayout()
        top_step_frequency_step_layout = QVBoxLayout()
        top_step_frequency_label = QLabel("Vertical Arm Step Frequency:")

        top_step_label = QLabel("Step:")
        self.top_step_frequency_step_spin = QSpinBox()
        self.top_step_frequency_step_spin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.top_step_frequency_step_spin.setRange(10, 1000)
        self.top_step_frequency_step_spin.setValue(10)
        self.top_step_frequency_step_spin.valueChanged.connect(
            lambda val: self.top_step_frequency_step_spin.setSingleStep( 90 if val == 10 else 900)
        )
        self.top_step_frequency_step_spin.setSingleStep(90)

        self.top_step_frequency_spin = QSpinBox()
        self.top_step_frequency_spin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.top_step_frequency_spin.setRange(
            self.MIN_STEP_FREQUENCY, self.MAX_STEP_FREQUENCY)
        self.top_freq_step = self.top_step_frequency_step_spin.value()
        self.top_step_frequency_step_spin.valueChanged.connect(
            lambda val: self.top_step_frequency_spin.setSingleStep(val)
        )
        self.top_step_frequency_spin.setValue(1000)
        self.top_step_frequency_spin.setSuffix(" Hz")
        
        top_step_frequency_layout.addWidget(top_step_frequency_label)
        top_step_frequency_layout.addWidget(self.top_step_frequency_spin)
        top_step_frequency_step_layout.addWidget(top_step_label)
        top_step_frequency_step_layout.addWidget(self.top_step_frequency_step_spin)
        top_step_layout.addLayout(top_step_frequency_layout)
        top_step_layout.addLayout(top_step_frequency_step_layout)

        bot_step_layout = QHBoxLayout()
        bot_step_frequency_layout = QVBoxLayout()
        bot_step_frequency_step_layout = QVBoxLayout()
        bot_step_frequency_label = QLabel("Horizontal Arm Step Frequency:")
        
        bot_step_label = QLabel("Step:")
        self.bot_step_frequency_step_spin = QSpinBox()
        self.bot_step_frequency_step_spin.setRange(10, 1000)
        self.bot_step_frequency_step_spin.setValue(10)
        self.bot_step_frequency_step_spin.valueChanged.connect(
            lambda val: self.bot_step_frequency_step_spin.setSingleStep( 90 if val == 10 else 900)
        )
        self.bot_step_frequency_step_spin.setSingleStep(90)

        self.bot_step_frequency_spin = QSpinBox()
        self.bot_step_frequency_spin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.bot_step_frequency_spin.setRange(
            self.MIN_STEP_FREQUENCY, self.MAX_STEP_FREQUENCY)
        self.bot_step_frequency_step_spin.valueChanged.connect(
            lambda val: self.bot_step_frequency_spin.setSingleStep(val)
        )
        self.bot_step_frequency_spin.setValue(1000)
        self.bot_step_frequency_spin.setSuffix(" Hz")

        bot_step_frequency_layout.addWidget(bot_step_frequency_label)
        bot_step_frequency_layout.addWidget(self.bot_step_frequency_spin)
        bot_step_frequency_step_layout.addWidget(bot_step_label)
        bot_step_frequency_step_layout.addWidget(self.bot_step_frequency_step_spin)
        bot_step_layout.addLayout(bot_step_frequency_layout)
        bot_step_layout.addLayout(bot_step_frequency_step_layout)

        btn_font = QFont()
        btn_font.setPointSize(14)

        def make_button(label: str) -> QPushButton:
            btn = QPushButton(label)
            btn.setFont(btn_font)
            btn.setMinimumSize(80,80)
            return btn

        self.btn_up = make_button("\u25b2")
        self.btn_down = make_button("\u25bc")
        self.btn_left = make_button("\u25c4")
        self.btn_right = make_button("\u25ba")

        top_motor.addWidget(self.btn_up)
        top_motor.addWidget(self.btn_down)
        bot_motor.addWidget(self.btn_left)
        bot_motor.addWidget(self.btn_right)
        button_layout.addLayout(bot_motor)
        button_layout.addLayout(top_motor)

        layout.addLayout(top_step_layout)
        layout.addLayout(bot_step_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.btn_up.pressed.connect(lambda: self._send(True, True, "A"))
        self.btn_up.released.connect(lambda: self._send(True, False, "A"))

        self.btn_down.pressed.connect(lambda: self._send(False, True, "A"))
        self.btn_down.released.connect(lambda: self._send(False, False, "A"))

        self.btn_left.pressed.connect(lambda: self._send(True, True, "B"))
        self.btn_left.released.connect(lambda: self._send(False, False, "B"))

        self.btn_right.pressed.connect(lambda: self._send(False, True, "B"))
        self.btn_right.released.connect(lambda: self._send(False, False, "B"))
        
        #Debug
        # self.set_enabled_controls(True)

    def _send(self, direction: bool, pulse: bool,  motor: str):
        match motor:
            case "A":
                frequency = self.top_step_frequency_spin.value()
            case "B":
                frequency = self.bot_step_frequency_spin.value()
        self.gpio_command.emit(direction, pulse, frequency, motor)

    def set_enabled_controls(self, enabled: bool):
        for btn in (self.btn_up, self.btn_down, self.btn_left, self.btn_right):
            btn.setEnabled(enabled)
        self.enabled = enabled

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if (a0.isAutoRepeat()):
            return

        key = a0.key()
        if self.enabled:
            match key:
                case Qt.Key.Key_PageUp:
                    self.btn_up.setDown(True)
                    self._send(True, True, "A")
                case Qt.Key.Key_PageDown:
                    self.btn_down.setDown(True)
                    self._send(False, True, "A")
                case Qt.Key.Key_BracketLeft:
                    self.btn_left.setDown(True)
                    self._send(True, True, "B")
                case Qt.Key.Key_BracketRight:
                    self.btn_right.setDown(True)
                    self._send(False, True, "B")
                case default:
                    super().keyPressEvent(a0)
        else: 
           super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent | None) -> None:
        if (a0.isAutoRepeat()):
            return

        key = a0.key()
        if self.enabled:
            match key:
                case Qt.Key.Key_PageUp:
                    self.btn_up.setDown(False)
                    self._send(True, False, "A")
                case Qt.Key.Key_PageDown:
                    self.btn_down.setDown(False)
                    self._send(False, False, "A")
                case Qt.Key.Key_BracketLeft:
                    self.btn_left.setDown(False)
                    self._send(False, False, "B")
                case Qt.Key.Key_BracketRight:
                    self.btn_right.setDown(False)
                    self._send(False, False, "B")
                case default:
                    super().keyReleaseEvent(a0)
        else:
            super().keyReleaseEvent(a0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = GPIOTeleopWidget()
    widget.show()
    sys.exit(app.exec())