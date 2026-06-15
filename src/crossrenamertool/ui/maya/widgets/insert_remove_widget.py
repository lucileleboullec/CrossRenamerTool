from PySide6 import QtCore, QtWidgets


class InsertRemovePage(QtWidgets.QWidget):
    """Widget for insert and remove page."""

    TITLE = "Insert/Remove"

    request_insert = QtCore.Signal(str, int, bool)
    request_remove = QtCore.Signal(int, int, bool)

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

        insert_group = QtWidgets.QGroupBox("Insert")
        insert_layout = QtWidgets.QGridLayout(insert_group)
        insert_layout.setSpacing(6)
        main_layout.addWidget(insert_group)

        insert_layout.addWidget(QtWidgets.QLabel("Text to insert:"), 0, 0)

        self.insert_text = QtWidgets.QLineEdit()
        self.insert_text.setToolTip(
            "<p>Text to insert at the given position.</p><p style='color: #95a5a6;'>Example: 'CTRL_' inserted at 0 ➞ CTRL_arm_L.</p>"
        )
        self.insert_text.setPlaceholderText("Characters to insert...")
        insert_layout.addWidget(self.insert_text, 0, 1, 1, 2)

        insert_layout.addWidget(QtWidgets.QLabel("Position:"), 1, 0)

        self.insert_position = QtWidgets.QSpinBox()
        self.insert_position.setToolTip(
            "<p>Position where the text will be inserted.</p><p> 0 = before the first/last character.</p>"
        )
        self.insert_position.setSingleStep(1)
        self.insert_position.setRange(0, 999)
        insert_layout.addWidget(self.insert_position, 1, 1)

        self.insert_from = QtWidgets.QComboBox()
        self.insert_from.setToolTip(
            "<p><b>From Start:</b> Insert from the start of the character.</p><p><b>From End:</b> Insert from the end of the character.</p>"
        )
        self.insert_from.addItems(["From Start", "From End"])
        insert_layout.addWidget(self.insert_from, 1, 2)

        insert_button = QtWidgets.QPushButton("Insert")
        insert_button.setToolTip(
            "<p>Insert the text at the given position.</p><p style='color: #95a5a6;'>Example: position=0, text='X_' from=From Start ➞ X_arm_L.</p><p style='color: #95a5a6;'>Example: position=0, text='_geo' from=From End ➞ arm_L_geo.</p>"
        )
        insert_button.setObjectName("primary")
        insert_button.clicked.connect(self._on_insert)
        insert_layout.addWidget(insert_button, 2, 0, 1, 3)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setObjectName("separator")
        main_layout.addWidget(separator)

        remove_group = QtWidgets.QGroupBox("Remove")
        remove_layout = QtWidgets.QGridLayout(remove_group)
        remove_layout.setSpacing(6)
        main_layout.addWidget(remove_group)

        remove_layout.addWidget(QtWidgets.QLabel("Position:"), 0, 0)
        self.remove_position = QtWidgets.QSpinBox()
        self.remove_position.setToolTip(
            "<p>Position where the text will be removed.</p><p> 0 = starts from the first/last character.</p>"
        )
        self.remove_position.setValue(0)
        self.remove_position.setRange(0, 999)
        self.remove_position.setSingleStep(1)
        remove_layout.addWidget(self.remove_position, 0, 1)

        self.remove_from = QtWidgets.QComboBox()
        self.remove_from.addItems(["From Start", "From End"])
        self.remove_from.setToolTip(
            "<p><b>From Start:</b> Remove from the start of the character.</p><p><b>From End:</b> Remove from the end of the character.</p>"
        )
        remove_layout.addWidget(self.remove_from, 0, 2)

        remove_layout.addWidget(QtWidgets.QLabel("Count:"), 1, 0)
        self.remove_count = QtWidgets.QSpinBox()
        self.remove_count.setToolTip("<p>Number of characters to delete.</p>")
        self.remove_count.setRange(1, 100)
        self.remove_count.setValue(1)
        self.remove_count.setSingleStep(1)
        remove_layout.addWidget(self.remove_count, 1, 1)

        remove_button = QtWidgets.QPushButton("Remove")
        remove_button.setToolTip(
            "<p>Delete characters.</p><p style='color: #95a5a6;'>Example: position=0, count=5 from=From Start  removes 'CTRL_' from 'CTRL_arm_L'.</p><p style='color: #95a5a6;'>Example: position=0, count=2 from=From End removes '_L' from 'arm_L'.</p>"
        )
        remove_button.setObjectName("danger")
        remove_button.clicked.connect(self._on_remove)
        remove_layout.addWidget(remove_button, 2, 0, 1, 3)

        main_layout.addStretch()

    def _on_insert(self) -> None:
        """Add characters to a text at a specific position."""
        text = self.insert_text.text()
        position = self.insert_position.value()
        from_start = self.insert_from.currentIndex() == 0

        self.request_insert.emit(text, position, from_start)

    def _on_remove(self) -> None:
        """Remove characters to a text at a specific position."""
        count = self.remove_count.value()
        position = self.remove_position.value()
        from_start = self.remove_from.currentIndex() == 0

        self.request_remove.emit(count, position, from_start)
