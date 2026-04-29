from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class SearchReplacePage(QtWidgets.QWidget):
    """Widget for search and replace nodes options."""

    TITLE = "Search/Replace"

    request_search_replace = QtCore.Signal(str, str, bool)

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

        search_row = QtWidgets.QHBoxLayout()
        search_row.addWidget(QtWidgets.QLabel("Search :"))
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        search_row.addWidget(self.search_field)
        main_layout.addLayout(search_row)

        replace_row = QtWidgets.QHBoxLayout()
        replace_row.addWidget(QtWidgets.QLabel("Replace :"))
        self.replace_field = QtWidgets.QLineEdit()
        self.replace_field.setPlaceholderText("Replace...")
        replace_row.addWidget(self.replace_field)
        main_layout.addLayout(replace_row)

        self.case = QtWidgets.QCheckBox("Case sensitive")
        self.case.setChecked(True)
        main_layout.addWidget(self.case)

        apply_btn = QtWidgets.QPushButton("Apply")
        apply_btn.clicked.connect(self._on_search_replace)
        main_layout.addWidget(apply_btn)

        main_layout.addStretch()

    def _on_search_replace(self):
        """Search name and replace by new one."""
        search_text = self.search_field.text()
        replace_text = self.replace_field.text()
        case = self.case.isChecked()
        self.request_search_replace.emit(search_text, replace_text, case)
