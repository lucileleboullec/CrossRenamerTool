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
        main_layout.setContentsMargins(12, 12, 12, 12)

        name_group = QtWidgets.QGroupBox("New Name")
        name_group_layout = QtWidgets.QVBoxLayout(name_group)
        name_group_layout.setSpacing(6)
        main_layout.addWidget(name_group)

        self.name_field = QtWidgets.QLineEdit()
        self.name_field.setPlaceholderText("Enter base name...")
        name_group_layout.addWidget(self.name_field)

        numbering_options_group = QtWidgets.QGroupBox("Numbering")
        numbering_options_group_layout = QtWidgets.QGridLayout(numbering_options_group)
        numbering_options_group_layout.setSpacing(8)
        main_layout.addWidget(numbering_options_group)

        numbering_options_group_layout.addWidget(QtWidgets.QLabel("Padding: "), 0, 0)
        self.padding = QtWidgets.QSpinBox()
        self.padding.setRange(1, 6)
        self.padding.setValue(constants.DEFAULT_PADDING)
        numbering_options_group_layout.addWidget(self.padding, 0, 1)

        numbering_options_group_layout.addWidget(QtWidgets.QLabel("Start at:"), 1, 0)
        self.start = QtWidgets.QSpinBox()
        self.start.setRange(0, 9999)
        self.start.setValue(constants.DEFAULT_START)
        numbering_options_group_layout.addWidget(self.start, 1, 1)

        numbering_options_group_layout.addWidget(QtWidgets.QLabel("Step :"), 2, 0)
        self.step = QtWidgets.QSpinBox()
        self.step.setValue(constants.DEFAULT_STEP)
        numbering_options_group_layout.addWidget(self.step, 2, 1)

        self.use_numbers = QtWidgets.QCheckBox("Append numbers")
        self.use_numbers.setChecked(True)
        numbering_options_group_layout.addWidget(self.use_numbers, 3, 0, 1, 2)

        # Preview
        preview_group = QtWidgets.QGroupBox("Preview")
        preview_layout = QtWidgets.QVBoxLayout(preview_group)
        self.preview_label = QtWidgets.QLabel("pCube_01, pCube_02, ...")
        self.preview_label.setStyleSheet(
            "color: #888888; font-style: italic; font-size: 11px;"
        )
        preview_layout.addWidget(self.preview_label)
        main_layout.addWidget(preview_group)

        self.name_field.textChanged.connect(self._update_preview)
        self.padding.valueChanged.connect(self._update_preview)
        self.start.valueChanged.connect(self._update_preview)
        self.step.valueChanged.connect(self._update_preview)
        self.use_numbers.toggled.connect(self._update_preview)

        main_layout.addStretch()

        rename_btn = QtWidgets.QPushButton("Rename")
        rename_btn.setObjectName("primary")
        rename_btn.setFixedHeight(32)
        rename_btn.clicked.connect(self._on_rename)
        main_layout.addWidget(rename_btn)

    def _on_rename(self):
        """Rename the selected nodes."""
        name = self.name_field.text()
        padding = self.padding.value()
        start = self.start.value()
        step = self.step.value()
        if not name:
            log.warning("Please enter a base name.")
            return
        self.request_rename.emit(name, padding, start, step)

    def _update_preview(self):
        """Update the preview."""
        name = self.name_field.text() or "node"
        padding = self.padding.value()
        start = self.start.value()
        step = self.step.value()
        if self.use_numbers.isChecked():
            exemples = [
                f"{name}_{str(start + i * step).zfill(padding)}" for i in range(3)
            ]
            self.preview_label.setText(", ".join(exemples) + ", ...")
        else:
            self.preview_label.setText(name)
