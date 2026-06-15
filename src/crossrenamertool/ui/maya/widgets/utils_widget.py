from PySide6 import QtCore, QtWidgets


class UtilsPage(QtWidgets.QWidget):
    """Widget for rename nodes options."""

    TITLE = "Name"

    request_rename_children_from_parent = QtCore.Signal()
    request_fix = QtCore.Signal(dict)
    request_auto_fix = QtCore.Signal()
    request_select_item = QtCore.Signal(int)
    request_refresh = QtCore.Signal()
    request_swap = QtCore.Signal()
    request_fix_shape_name = QtCore.Signal()

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
        main_layout.setSpacing(8)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)

        container = QtWidgets.QWidget()
        c_layout = QtWidgets.QVBoxLayout(container)
        c_layout.setSpacing(8)
        c_layout.setContentsMargins(0, 0, 0, 0)

        children_group = QtWidgets.QGroupBox("Rename Children from Parent")
        children_layout = QtWidgets.QVBoxLayout(children_group)
        c_layout.addWidget(children_group)

        children_label = QtWidgets.QLabel(
            "Renames all child nodes using their parent's name as base, appending an index."
        )
        children_label.setStyleSheet("color: #888888; font_size: 11px;")
        children_layout.addWidget(children_label)
        children_button = QtWidgets.QPushButton("Rename Children")
        children_button.setToolTip(
            "<p>Rename direct children of the selected node using the parent name.</p><p style='color: #95a5a6;'>Exemple: GRP_arm_L ➞ GRP_arm_L_001, GRP_arm_L_002</p>"
        )
        children_button.setObjectName("primary")
        children_button.clicked.connect(self._on_rename_children_from_parent)
        children_layout.addWidget(children_button)

        duplicate_group = QtWidgets.QGroupBox("Fix Duplicate Naming")
        duplicate_layout = QtWidgets.QGridLayout(duplicate_group)
        c_layout.addWidget(duplicate_group)

        duplicate_label = QtWidgets.QLabel("Renames nodes that were duplicated.")
        duplicate_label.setStyleSheet("color: #888888; font_size: 11px;")
        duplicate_layout.addWidget(duplicate_label, 0, 0, 1, 2)

        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.setToolTip(
            "<p>Refresh the duplicates list from the current scene.</p>"
        )
        refresh_button.clicked.connect(self._on_refresh)
        duplicate_layout.addWidget(refresh_button, 1, 0)

        self.duplicates_table = self._set_list()
        self.duplicates_table.setToolTip(
            "<p>List of nodes with duplicates names in the scenes.</p><p>Edit the 'New Name' column to set a custom name before applying.</p>"
        )
        self.duplicates_table.setMinimumHeight(200)
        self.duplicates_table.setColumnCount(2)
        self.duplicates_table.setHorizontalHeaderLabels(["Current Name", "New Name"])
        header = self.duplicates_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.duplicates_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.duplicates_table.clicked.connect(self._on_item_changed)
        duplicate_layout.addWidget(self.duplicates_table, 2, 0, 1, 2)

        auto_fix_button = QtWidgets.QPushButton("Auto Fix Duplicates")
        auto_fix_button.setToolTip(
            "<p>Automatically rename all duplicates using their hierarchy path.</p><p style='color: #95a5a6;'>Exemple: arm ➞ GRP_arm_L_001.</p>"
        )
        auto_fix_button.setObjectName("primary")
        auto_fix_button.clicked.connect(self._on_auto_fix_button)
        duplicate_layout.addWidget(auto_fix_button, 3, 0)

        fix_button = QtWidgets.QPushButton("Fix Duplicate")
        fix_button.setToolTip(
            "<p>Rename duplicates using the names entered in the 'New Name' column.</p>"
        )
        fix_button.clicked.connect(self._on_fix_button)
        duplicate_layout.addWidget(fix_button, 3, 1)

        shape_group = QtWidgets.QGroupBox("Fix Shape Names")
        shape_layout = QtWidgets.QVBoxLayout(shape_group)
        c_layout.addWidget(shape_group)

        shape_label = QtWidgets.QLabel(
            "Renames shape nodes to match their transform parent (e.g. pCube1 -> pCube1Shape)."
        )
        shape_label.setStyleSheet("color: #888888; font_size: 11px;")
        shape_layout.addWidget(shape_label)

        shape_button = QtWidgets.QPushButton("Fix Shapes")
        shape_button.setToolTip(
            "<p>Rename all shapes nodes to match their transform name.</p><p style='color: #95a5a6;'>Exemple: pCubeShape1 under arm_geo ➞ arm_geoShape.</p>"
        )
        shape_button.setObjectName("primary")
        shape_button.clicked.connect(self._on_fix_shape_name)
        shape_layout.addWidget(shape_button)

        swap_group = QtWidgets.QGroupBox("Swap Side Indicators")
        swap_layout = QtWidgets.QVBoxLayout(swap_group)
        c_layout.addWidget(swap_group)

        swap_label = QtWidgets.QLabel(
            "Swap left/right indicators (L<->R, Left<->Right,etc.)."
        )
        swap_label.setStyleSheet("color: #888888; font_size: 11px;")
        swap_layout.addWidget(swap_label)

        swap_button = QtWidgets.QPushButton("Swap L <-> R")
        swap_button.setToolTip(
            "<p>Swap left and right side indicators in node names.</p><p style='color: #95a5a6;'>Exemple: Supports; L/R, l/r, Left/Right, left/right, LEFT/RIGHT.</p>"
        )
        swap_button.setObjectName("primary")
        swap_button.clicked.connect(self._on_swap)
        swap_layout.addWidget(swap_button)

        c_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _on_rename_children_from_parent(self) -> None:
        """Rename the selected nodes."""
        self.request_rename_children_from_parent.emit()

    def _on_refresh(self) -> None:
        """Refresh the duplicates list from the current scene."""
        self.request_refresh.emit()

    def _on_auto_fix_button(self) -> None:
        """Automatically rename all duplicates using the hierarchy path."""
        self.request_auto_fix.emit()

    def _on_fix_button(self) -> None:
        """Rename duplicates using the names entered."""
        items = {}
        for row in range(self.duplicates_table.rowCount()):
            old_name = self.duplicates_table.item(row, 0).text()
            new_name = self.duplicates_table.item(row, 1).text().strip()

            if new_name:
                items[old_name] = new_name

        self.request_fix.emit(items)

    def _set_list(self) -> QtWidgets.QTableWidget:
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

    def _on_item_changed(self, index) -> None:
        """Select node by the duplicates table."""
        if index.column() == 0:
            self.request_select_item.emit(index.row())

    def _on_swap(self) -> None:
        """Swap side indicator on nodes."""
        self.request_swap.emit()

    def _on_fix_shape_name(self) -> None:
        """Rename shapes to match their transform name."""
        self.request_fix_shape_name.emit()
