from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants


class UtilsPage(QtWidgets.QWidget):
    """Widget for rename nodes options."""

    TITLE = "Name"

    request_rename_children_from_parent = QtCore.Signal(int)
    request_fix = QtCore.Signal(list)
    request_auto_fix = QtCore.Signal()
    request_select_item = QtCore.Signal(int)
    request_refresh = QtCore.Signal()
    request_swap = QtCore.Signal()

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
        name_row.addWidget(QtWidgets.QLabel("Children :"))
        main_layout.addLayout(name_row)

        name_options_row = QtWidgets.QHBoxLayout()
        name_options_row.addWidget(QtWidgets.QLabel("Padding :"))
        main_layout.addLayout(name_options_row)

        self.padding = QtWidgets.QSpinBox()
        self.padding.setRange(1, 5)
        self.padding.setValue(constants.DEFAULT_PADDING)
        name_options_row.addWidget(self.padding)

        rename_btn = QtWidgets.QPushButton("Rename Children from Parent")
        rename_btn.clicked.connect(self._on_rename_children_from_parent)
        main_layout.addWidget(rename_btn)
        main_layout.addStretch()

        duplicates_row = QtWidgets.QGridLayout()
        duplicates_row.addWidget(QtWidgets.QLabel("Fix Duplicates :"), 0, 0)
        main_layout.addLayout(duplicates_row)

        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(self._on_refresh)
        duplicates_row.addWidget(refresh_button, 1, 0)

        self.duplicates_table = self._set_list()
        self.duplicates_table.setColumnCount(2)
        self.duplicates_table.setHorizontalHeaderLabels(["Current Name", "New Name"])
        header = self.duplicates_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.duplicates_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.duplicates_table.currentItemChanged.connect(self._on_item_changed)
        duplicates_row.addWidget(self.duplicates_table, 2, 0, 1, 2)

        auto_fix_button = QtWidgets.QPushButton("Auto Rename Duplicates")
        auto_fix_button.clicked.connect(self._on_auto_fix_button)
        duplicates_row.addWidget(auto_fix_button, 3, 0)

        fix_button = QtWidgets.QPushButton("Rename Selected")
        fix_button.clicked.connect(self._on_fix_button)
        duplicates_row.addWidget(fix_button, 3, 1)

        quick_fixes_row = QtWidgets.QGridLayout()
        quick_fixes_row.addWidget(QtWidgets.QLabel("Quick Fixes :"), 0, 0)
        main_layout.addLayout(quick_fixes_row)

        swap_button = QtWidgets.QPushButton("Swap L <-> R")
        swap_button.clicked.connect(self._on_swap)
        quick_fixes_row.addWidget(swap_button, 1, 1)

    def _on_rename_children_from_parent(self):
        """Rename the selected nodes."""
        padding = self.padding.value()
        self.request_rename_children_from_parent.emit(padding)

    def _on_refresh(self):
        self.request_refresh.emit()

    def _on_auto_fix_button(self):
        self.request_auto_fix.emit()

    def _on_fix_button(self):
        items = [
            self.duplicates_table.item(index, 1).text()
            for index in range(self.duplicates_table.rowCount())
        ]

        self.request_fix.emit(items)

    def _set_list(self):
        """Set the list.

        Returns:
            QtWidgets.QListWidget(): ListWidget

        """
        return QtWidgets.QTableWidget()

    def ingest_list(self, duplicates, filters: dict = None) -> None:
        """Ingest playblast in the list.

        Args:
            filters (dict, optional): text for filter the list. Defaults to None.

        """
        self.duplicates_table.setRowCount(0)

        for data, short_name in duplicates.items():
            row = self.duplicates_table.rowCount()
            self.duplicates_table.insertRow(row)

            item_current = QtWidgets.QTableWidgetItem(data)
            item_current.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.duplicates_table.setItem(row, 0, item_current)

            item_new = QtWidgets.QTableWidgetItem(short_name)
            item_new.setFlags(
                QtCore.Qt.ItemIsSelectable
                | QtCore.Qt.ItemIsEnabled
                | QtCore.Qt.ItemIsEditable  # éditable
            )
            self.duplicates_table.setItem(row, 1, item_new)

    def _on_item_changed(self):
        """Select node by the duplicates table."""
        index = self.duplicates_table.currentRow()
        self.request_select_item.emit(index)

    def _on_swap(self):
        """Swap side indicator on nodes."""
        self.request_swap.emit()
