from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class InsertRemovePage(QtWidgets.QWidget):
    """Widget for insert and remove page."""

    TITLE = "Insert/Remove"

    request_start_insert = QtCore.Signal(str, int)
    request_end_insert = QtCore.Signal(str, int)
    request_start_remove = QtCore.Signal(int, int)
    request_end_remove = QtCore.Signal(int, int)

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

        insert_character_row = QtWidgets.QHBoxLayout()
        insert_character_row.addWidget(QtWidgets.QLabel("Insert:"))
        self.start_insert_character = QtWidgets.QSpinBox()
        self.start_insert_character.setSingleStep(1)
        insert_character_row.addWidget(self.start_insert_character)

        insert_start_btn = QtWidgets.QPushButton("+")
        insert_start_btn.clicked.connect(self._on_insert_start_character)
        insert_character_row.addWidget(insert_start_btn)

        self.text_to_add = QtWidgets.QLineEdit()
        self.text_to_add.setPlaceholderText("Text to add...")
        insert_character_row.addWidget(self.text_to_add)

        insert_end_btn = QtWidgets.QPushButton("+")
        insert_end_btn.clicked.connect(self._on_insert_end_character)
        insert_character_row.addWidget(insert_end_btn)

        self.add_end_character = QtWidgets.QSpinBox()
        self.add_end_character.setSingleStep(1)
        insert_character_row.addWidget(self.add_end_character)

        main_layout.addLayout(insert_character_row)

        main_layout.addStretch()

        remove_character_row = QtWidgets.QHBoxLayout()
        remove_character_row.addWidget(QtWidgets.QLabel("Remove:"))
        self.start_remove_character = QtWidgets.QSpinBox()
        self.start_remove_character.setSingleStep(1)
        remove_character_row.addWidget(self.start_remove_character)

        remove_start_btn = QtWidgets.QPushButton("-")
        remove_start_btn.clicked.connect(self._on_remove_start_character)
        remove_character_row.addWidget(remove_start_btn)

        self.count_characters = QtWidgets.QSpinBox()
        self.count_characters.setSingleStep(1)
        remove_character_row.addWidget(self.count_characters)

        remove_end_btn = QtWidgets.QPushButton("-")
        remove_end_btn.clicked.connect(self._on_remove_end_character)
        remove_character_row.addWidget(remove_end_btn)

        self.end_remove_character = QtWidgets.QSpinBox()
        self.end_remove_character.setSingleStep(1)
        remove_character_row.addWidget(self.end_remove_character)

        main_layout.addLayout(remove_character_row)

        main_layout.addStretch()

    def _on_insert_start_character(self):
        """Add characters to a text at a specific position by the start."""
        text = self.text_to_add.text()
        position = self.start_insert_character.value()

        self.request_start_insert.emit(text, position)

    def _on_insert_end_character(self):
        """Add characters to a text at a specific position by the end."""
        text = self.text_to_add.text()
        position = self.add_end_character.value()

        self.request_end_insert.emit(text, position)

    def _on_remove_start_character(self):
        """Remove characters to a text at a specific position by the start."""
        count = self.count_characters.value()
        position = self.start_remove_character.value()

        self.request_start_remove.emit(count, position)

    def _on_remove_end_character(self):
        """Add Remove to a text at a specific position by the end."""
        count = self.count_characters.value()
        position = self.end_remove_character.value()

        self.request_end_remove.emit(count, position)
