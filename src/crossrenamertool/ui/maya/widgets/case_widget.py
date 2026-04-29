from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class CasePage(QtWidgets.QWidget):
    """Widget for case sensitive page."""

    TITLE = "Case"

    request_lowercase = QtCore.Signal()
    request_uppercase = QtCore.Signal()
    request_capitalize = QtCore.Signal()

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

        case_sensitive_row = QtWidgets.QHBoxLayout()
        lowercase_btn = QtWidgets.QPushButton("Lowercase")
        lowercase_btn.clicked.connect(self._on_lowercase)
        case_sensitive_row.addWidget(lowercase_btn)

        uppercase_btn = QtWidgets.QPushButton("Uppercase")
        uppercase_btn.clicked.connect(self._on_uppercase)
        case_sensitive_row.addWidget(uppercase_btn)

        capitalize_btn = QtWidgets.QPushButton("Capitalize")
        capitalize_btn.clicked.connect(self._on_capitalize)
        case_sensitive_row.addWidget(capitalize_btn)

        main_layout.addLayout(case_sensitive_row)
        main_layout.addStretch()

    def _on_lowercase(self):
        """Convert text to lowercase."""
        self.request_lowercase.emit()

    def _on_uppercase(self):
        """Convert text to uppercase."""
        self.request_uppercase.emit()

    def _on_capitalize(self):
        """Convert text to capitalize."""
        self.request_capitalize.emit()
