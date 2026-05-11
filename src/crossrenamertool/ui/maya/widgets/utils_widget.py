from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class UtilsPage(QtWidgets.QWidget):
    """Widget for rename nodes options."""

    TITLE = "Name"

    request_rename_children_from_parent = QtCore.Signal(int)
    request_fix = QtCore.Signal(list)
    request_auto_fix = QtCore.Signal()

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

        duplicates_row = QtWidgets.QVBoxLayout()
        duplicates_row.addWidget(QtWidgets.QLabel("Fix Duplicates :"))
        main_layout.addLayout(duplicates_row)

        self.list_duplicates = self._set_list()
        duplicates_row.addWidget(self.list_duplicates)

        auto_fix_button = QtWidgets.QPushButton("Auto Fix Duplicates")
        auto_fix_button.clicked.connect(self._on_auto_fix_button)
        duplicates_row.addWidget(auto_fix_button)

        fix_button = QtWidgets.QPushButton("Fix Duplicates")
        fix_button.clicked.connect(self._on_fix_button)
        duplicates_row.addWidget(fix_button)

    def _on_rename_children_from_parent(self):
        """Rename the selected nodes."""
        padding = self.padding.value()
        self.request_rename_children_from_parent.emit(padding)

    def _on_auto_fix_button(self):
        self.request_auto_fix.emit()

    def _on_fix_button(self):
        items = [
            self.list_duplicates.item(index).text()
            for index in range(self.list_duplicates.count())
        ]

        self.request_fix.emit(items)

    def _set_list(self):
        """Set the list.

        Returns:
            QtWidgets.QListWidget(): ListWidget

        """
        return QtWidgets.QListWidget()

    def ingest_list(self, datas, filters: dict = None) -> None:
        """Ingest playblast in the list.

        Args:
            filters (dict, optional): text for filter the list. Defaults to None.

        """
        self.list_duplicates.clear()

        for data in datas:
            item = QtWidgets.QListWidgetItem(data)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.list_duplicates.addItem(item)
