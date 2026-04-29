from PySide6 import QtCore, QtGui, QtWidgets
import logging

from crossrenamertool.core import constants

log = logging.getLogger(__name__)


class RenamePage(QtWidgets.QWidget):
    """Widget for rename nodes options."""

    TITLE = "Name"

    request_rename = QtCore.Signal(str, int, int, int)

    def __init__(self, parent=None):
        """Initialize the widget."""
        super().__init__(parent=parent)

        self._configure()
        self._create_gui()

    def _configure(self):
        """Configure the widget."""
        self.setWindowTitle(self.TITLE)

    def _create_gui(self):
        """Create the GUI."""
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 8, 0, 8)

        name_row = QtWidgets.QHBoxLayout()
        name_row.addWidget(QtWidgets.QLabel("Name :"))
        self.name_field = QtWidgets.QLineEdit()
        self.name_field.setPlaceholderText("New Name...")
        name_row.addWidget(self.name_field)
        main_layout.addLayout(name_row)

        name_options_row = QtWidgets.QHBoxLayout()
        name_options_row.addWidget(QtWidgets.QLabel("Padding :"))
        main_layout.addLayout(name_options_row)

        self.padding = QtWidgets.QSpinBox()
        self.padding.setRange(1, 5)
        self.padding.setValue(constants.DEFAULT_PADDING)
        name_options_row.addWidget(self.padding)

        name_options_row.addWidget(QtWidgets.QLabel("Start :"))
        self.start = QtWidgets.QSpinBox()
        self.start.setRange(0, 9999)
        self.start.setValue(constants.DEFAULT_START)
        name_options_row.addWidget(self.start)

        name_options_row.addWidget(QtWidgets.QLabel("Step :"))
        self.step = QtWidgets.QSpinBox()
        self.step.setValue(constants.DEFAULT_STEP)
        name_options_row.addWidget(self.step)

        rename_btn = QtWidgets.QPushButton("Rename")
        rename_btn.clicked.connect(self._on_rename)
        main_layout.addWidget(rename_btn)
        main_layout.addStretch()

    def _on_rename(self):
        """Rename the selected nodes."""
        name = self.name_field.text()
        padding = self.padding.value()
        start = self.start.value()
        step = self.step.value()
        if not name:
            log.warning("Please enter a name before renaming.")
            return
        self.request_rename.emit(name, padding, start, step)
