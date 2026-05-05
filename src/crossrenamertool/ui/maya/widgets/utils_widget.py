from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class UtilsPage(QtWidgets.QWidget):
    """Widget for rename nodes options."""

    TITLE = "Name"

    request_rename_children_from_parent = QtCore.Signal(int)

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
        name_row.addWidget(QtWidgets.QLabel("Rename Children from Parent :"))
        main_layout.addLayout(name_row)

        name_options_row = QtWidgets.QHBoxLayout()
        name_options_row.addWidget(QtWidgets.QLabel("Padding :"))
        main_layout.addLayout(name_options_row)

        self.padding = QtWidgets.QSpinBox()
        self.padding.setRange(1, 5)
        self.padding.setValue(constants.DEFAULT_PADDING)
        name_options_row.addWidget(self.padding)

        rename_btn = QtWidgets.QPushButton("Rename children from parent")
        rename_btn.clicked.connect(self._on_rename_children_from_parent)
        main_layout.addWidget(rename_btn)
        main_layout.addStretch()

    def _on_rename_children_from_parent(self):
        """Rename the selected nodes."""
        padding = self.padding.value()
        self.request_rename_children_from_parent.emit(padding)
