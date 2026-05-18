from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class SearchReplacePage(QtWidgets.QWidget):
    """Widget for search and replace nodes options."""

    TITLE = "Search/Replace"

    request_search_replace = QtCore.Signal(str, str, bool, bool)
    request_preview_search_replace = QtCore.Signal(str, str, bool, bool)

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

        search_replace_group = QtWidgets.QGroupBox("Search & Replace")
        search_replace_layout = QtWidgets.QGridLayout(search_replace_group)
        search_replace_layout.setSpacing(8)
        main_layout.addWidget(search_replace_group)

        search_replace_layout.addWidget(QtWidgets.QLabel("Search:"), 0, 0)
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.setPlaceholderText("Text to find...")
        search_replace_layout.addWidget(self.search_field, 0, 1)

        search_replace_layout.addWidget(QtWidgets.QLabel("Replace:"), 1, 0)
        self.replace_field = QtWidgets.QLineEdit()
        self.replace_field.setPlaceholderText("Replace with... (empty = delete)")
        search_replace_layout.addWidget(self.replace_field, 1, 1)

        options_row = QtWidgets.QHBoxLayout()
        self.case = QtWidgets.QCheckBox("Case sensitive")
        self.case.setChecked(True)
        options_row.addWidget(self.case)

        self.regex = QtWidgets.QCheckBox("Regex")
        self.regex.setChecked(False)
        options_row.addWidget(self.regex)
        options_row.addStretch()
        search_replace_layout.addLayout(options_row, 2, 0, 1, 2)

        preview_group = QtWidgets.QGroupBox("Preview")
        preview_layout = QtWidgets.QVBoxLayout(preview_group)
        main_layout.addWidget(preview_group)
        self.preview_label = QtWidgets.QLabel("-")
        self.preview_label.setStyleSheet("color: #888888; font-size: 11px;")
        self.preview_label.setWordWrap(True)
        preview_layout.addWidget(self.preview_label)

        self.search_field.textChanged.connect(self._update_preview)
        self.replace_field.textChanged.connect(self._update_preview)
        self.case.toggled.connect(self._update_preview)
        self.regex.toggled.connect(self._update_preview)

        main_layout.addStretch()

        apply_btn = QtWidgets.QPushButton("Apply Replace")
        apply_btn.setFixedHeight(32)
        apply_btn.clicked.connect(self._on_search_replace)
        main_layout.addWidget(apply_btn)

    def _on_search_replace(self):
        """Search name and replace by new one."""
        search_text = self.search_field.text()
        replace_text = self.replace_field.text()
        case = self.case.isChecked()
        regex = self.regex.isChecked()
        self.request_search_replace.emit(search_text, replace_text, case, regex)

    def _update_preview(self):
        search = self.search_field.text()
        replace = self.replace_field.text()
        case = self.case.isChecked()
        regex = self.regex.isChecked()

        if not search:
            self.preview_label.setText("-")
            return
        self.request_preview_search_replace.emit(search, replace, case, regex)
