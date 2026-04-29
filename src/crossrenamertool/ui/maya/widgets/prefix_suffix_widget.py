from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class PrefixSuffixPage(QtWidgets.QWidget):
    """Widget for prefix and suffix options."""

    TITLE = "Prefix/Suffix"

    request_prefix = QtCore.Signal(str)
    request_suffix = QtCore.Signal(str)

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

        # Prefix
        prefix_row = QtWidgets.QHBoxLayout()
        prefix_row.addWidget(QtWidgets.QLabel("Prefix :"))
        self.prefix = QtWidgets.QComboBox()
        self.prefix.addItems(constants.PREFIXES)
        self.prefix.setEditable(True)
        self.prefix.setCurrentIndex(-1)
        self.prefix.lineEdit().setPlaceholderText("ex: CTRL")
        prefix_row.addWidget(self.prefix)
        add_prefix_btn = QtWidgets.QPushButton("Add")
        add_prefix_btn.setFixedWidth(50)
        add_prefix_btn.clicked.connect(self._on_add_prefix)
        prefix_row.addWidget(add_prefix_btn)
        main_layout.addLayout(prefix_row)

        # Suffix
        suffix_row = QtWidgets.QHBoxLayout()
        suffix_row.addWidget(QtWidgets.QLabel("Suffix :"))
        self.suffix = QtWidgets.QComboBox()
        self.suffix.addItems(constants.SUFFIXES)
        self.suffix.setEditable(True)
        self.suffix.setCurrentIndex(-1)
        self.suffix.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.suffix.lineEdit().setPlaceholderText("ex: geo")
        suffix_row.addWidget(self.suffix)
        add_suffix_btn = QtWidgets.QPushButton("Add")
        add_suffix_btn.setFixedWidth(50)
        add_suffix_btn.clicked.connect(self._on_add_suffix)
        suffix_row.addWidget(add_suffix_btn)
        main_layout.addLayout(suffix_row)

        main_layout.addStretch()

    def _on_add_prefix(self):
        """Add prefix to the node name."""
        prefix = self.prefix.currentText()
        self.request_prefix.emit(prefix)

    def _on_add_suffix(self):
        """Add suffix to the node name."""
        suffix = self.suffix.currentText()
        self.request_suffix.emit(suffix)
