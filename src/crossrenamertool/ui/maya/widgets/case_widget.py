from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class CasePage(QtWidgets.QWidget):
    """Widget for case sensitive page."""

    TITLE = "Case"

    request_lowercase = QtCore.Signal()
    request_uppercase = QtCore.Signal()
    request_capitalize = QtCore.Signal()
    request_title = QtCore.Signal()
    request_camel = QtCore.Signal()
    request_pascal = QtCore.Signal()
    request_snake = QtCore.Signal()

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
        main_layout.setSpacing(10)

        case_group = QtWidgets.QGroupBox("Case Conversion")
        case_layout = QtWidgets.QVBoxLayout(case_group)
        case_layout.setSpacing(8)
        main_layout.addWidget(case_group)

        cases = [
            ("lowercase", "all lowercase", self._on_lowercase),
            ("UPPERCASE", "ALL UPPERCASE", self._on_uppercase),
            ("Title", "First Letter Of Each Word", self._on_title),
            ("Capitalize", "First letter only", self._on_capitalize),
            ("camelCase", "camelCase (split on _ and -)", self._on_camel),
            ("PascalCase", "PascalCase (split on _ and -)", self._on_pascal),
            ("snake_case", "snake_case (split on uppercase)", self._on_snake),
        ]

        for label, tooltip, function in cases:
            row = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(f"<b>{label}</b>")
            label.setFixedWidth(120)
            label.setToolTip(tooltip)
            row.addWidget(label)

            exemple_label = QtWidgets.QLabel(f"<i>{tooltip}</i>")
            exemple_label.setStyleSheet("color: #888888; font-size: 11px;")
            row.addWidget(exemple_label)

            button = QtWidgets.QPushButton("Apply")
            button.setFixedWidth(60)
            button.clicked.connect(function)
            row.addWidget(button)
            case_layout.addLayout(row)

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

    def _on_title(self):
        """Convert text to title."""
        self.request_title.emit()

    def _on_camel(self):
        """Convert text to camel."""
        self.request_camel.emit()

    def _on_pascal(self):
        """Convert text to pascal."""
        self.request_pascal.emit()

    def _on_snake(self):
        """Convert text to snake."""
        self.request_snake.emit()
