from PySide6 import QtCore, QtWidgets


class SearchReplacePage(QtWidgets.QWidget):
    """Widget for search and replace nodes options."""

    TITLE = "Search/Replace"

    request_search_replace = QtCore.Signal(str, str, bool, bool)
    request_preview_search_replace = QtCore.Signal(str, str, bool, bool)

    def __init__(self, parent=None) -> None:
        """Initialize the widget."""
        super().__init__(parent=parent)

        self._configure()
        self._create_gui()

    def _configure(self) -> None:
        """Configure the widget."""
        self.setWindowTitle(self.TITLE)

    def _create_gui(self) -> None:
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
        self.search_field.setToolTip(
            "<p>Text to search for in the node names.</p><p>Supports partial matches.</p>"
        )
        self.search_field.setPlaceholderText("Text to find...")
        search_replace_layout.addWidget(self.search_field, 0, 1)

        search_replace_layout.addWidget(QtWidgets.QLabel("Replace:"), 1, 0)
        self.replace_field = QtWidgets.QLineEdit()
        self.replace_field.setToolTip(
            "<p>Text to replace the search term with.</p><p>Leave empty to delete the search term.</p>"
        )
        self.replace_field.setPlaceholderText("Replace with... (empty = delete)")
        search_replace_layout.addWidget(self.replace_field, 1, 1)

        options_row = QtWidgets.QHBoxLayout()
        self.case = QtWidgets.QCheckBox("Case sensitive")
        self.case.setToolTip(
            "<p><b>Checked:</b> terms with different cases are treated as different.</p><p style='color: #95a5a6;'>Example: 'Arm' and 'arm' are not the same.</p><p><b>Unchecked:</b> terms are matched regardless of case.</p><p style='color: #95a5a6;'>Example: 'Arm', 'ARM' and 'arm' all matches.</p>",
        )
        self.case.setChecked(True)
        options_row.addWidget(self.case)

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

        main_layout.addStretch()

        apply_btn = QtWidgets.QPushButton("Apply Replace")
        apply_btn.setToolTip(
            "<p>Apply the search and replace to all matching nodes.</p>"
        )
        apply_btn.setObjectName("primary")
        apply_btn.setFixedHeight(32)
        apply_btn.clicked.connect(self._on_search_replace)
        main_layout.addWidget(apply_btn)

    def _on_search_replace(self) -> None:
        """Search name and replace by new one."""
        search_text = self.search_field.text()
        replace_text = self.replace_field.text()
        case = self.case.isChecked()
        self.request_search_replace.emit(search_text, replace_text, case)

    def _update_preview(self) -> None:
        search = self.search_field.text()
        replace = self.replace_field.text()
        case = self.case.isChecked()

        if not search:
            self.preview_label.setText("-")
            return
        self.request_preview_search_replace.emit(search, replace, case)
