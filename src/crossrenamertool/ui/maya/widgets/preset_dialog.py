import importlib
import logging

from PySide6 import QtCore, QtWidgets

from crossrenamertool.core import constants
from crossrenamertool.core import presets as presets_manager

importlib.reload(presets_manager)
importlib.reload(constants)
log = logging.getLogger(__name__)


class PresetsDialog(QtWidgets.QDialog):
    """Dialog for managing prefix and suffis presets."""

    TITLE = "Manage Presets"

    prefixes_changed = QtCore.Signal(list)
    suffixes_changed = QtCore.Signal(list)

    def __init__(self, parent=None, stylesheet=""):
        super().__init__(parent)

        self.stylesheet = stylesheet

        self._configure()
        self._create_gui()
        self._load()

    def _configure(self):
        """Configure the widget."""
        self.setWindowTitle(self.TITLE)
        if self.stylesheet:
            self.setStyleSheet(self.stylesheet)
        self.setMinimumWidth(420)
        self.setModal(True)

    def _create_gui(self):
        """Create the GUI."""
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        columns_layout = QtWidgets.QHBoxLayout()
        columns_layout.setSpacing(16)

        self.prefix_list = self._create_column(
            label="Prefixes",
            layout=columns_layout,
            on_add=self._on_add_prefix,
            on_remove=self._on_remove_prefix,
        )

        self.suffix_list = self._create_column(
            label="Suffixes",
            layout=columns_layout,
            on_add=self._on_add_suffix,
            on_remove=self._on_remove_suffix,
        )

        main_layout.addLayout(columns_layout)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line)

        bottom_layout = QtWidgets.QHBoxLayout()

        reset_btn = QtWidgets.QPushButton("Reset to defaults")
        reset_btn.setToolTip("Restore the default presets list.")
        reset_btn.clicked.connect(self._on_reset)
        bottom_layout.addWidget(reset_btn)

        bottom_layout.addStretch()

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setDefault(True)
        close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(close_btn)

        main_layout.addLayout(bottom_layout)

    def _create_column(self, label, layout, on_add, on_remove):
        """Create a preset column with a list and add/remove buttons.

        Args:
            label (str): column title
            layout (QLayout): parent layout
            on_add (callable): callback for add button
            on_remove (callable): callback for remove button

        Returns:
            QListWidget: list widget

        """
        col_layout = QtWidgets.QVBoxLayout()
        col_layout.setSpacing(6)

        col_layout.addWidget(QtWidgets.QLabel(f"<b>{label}</b>"))

        list_widget = QtWidgets.QListWidget()
        list_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        list_widget.setToolTip("Drag too reorder. Double-click to rename.")
        col_layout.addWidget(list_widget)

        input_row = QtWidgets.QHBoxLayout()
        input_row.setSpacing(4)

        field = QtWidgets.QLineEdit()
        field.setPlaceholderText(f"New {label[:-1].lower()}...")
        input_row.addWidget(field)

        add_btn = QtWidgets.QPushButton("+")
        add_btn.setObjectName("primary")
        add_btn.setFixedWidth(30)
        add_btn.setToolTip(f"Add a new {label[:-1].lower()} preset.")
        add_btn.clicked.connect(lambda: on_add(field, list_widget))

        field.returnPressed.connect(lambda: on_add(field, list_widget))

        input_row.addWidget(add_btn)
        col_layout.addLayout(input_row)

        remove_btn = QtWidgets.QPushButton("Remove selected")
        remove_btn.setToolTip(f"Remove the selected {label[:-1].lower()} from presets.")
        remove_btn.clicked.connect(lambda: on_remove(list_widget))
        remove_btn.setObjectName("danger")
        col_layout.addWidget(remove_btn)

        layout.addLayout(col_layout)

        list_widget.model().rowsMoved.connect(
            lambda: self._on_order_changed(list_widget, label)
        )

        list_widget.itemDoubleClicked.connect(lambda item: list_widget.editItem(item))

        list_widget.itemChanged.connect(
            lambda: self._on_item_renamed(list_widget, label)
        )

        return list_widget

    def _load(self):
        """Load presets into both lists."""
        self._populate(self.prefix_list, presets_manager.load_presets("prefixes"))
        self._populate(self.suffix_list, presets_manager.load_presets("suffixes"))

    def _populate(self, list_widget, items):
        """Fill a list widget with items.

        Args:
            list_widget (QListWidget): the list to populate
            items (list[str]): items to add

        """
        list_widget.clear()
        for item in items:
            widget_item = QtWidgets.QListWidgetItem(item)
            widget_item.setFlags(widget_item.flags() | QtCore.Qt.ItemIsEditable)
            list_widget.addItem(widget_item)

    def _on_add_prefix(self, field, list_widget):
        """Add a new prefix preset.

        Args:
            field (QLineEdit): input field
            list_widget (QListWidget): the list to update

        """
        value = field.text().strip()
        if not value:
            return

        existing = self._get_items(list_widget)
        if value in existing:
            self._show_warning(f"'{value}' already exists in prefixes.")
            return

        presets_manager.add_prefixes(value)
        self._populate(list_widget, presets_manager.load_presets("prefixes"))
        self.prefixes_changed.emit(presets_manager.load_presets("prefixes"))
        field.clear()

    def _on_remove_prefix(self, list_widget):
        """Remove selected prefix preset.

        Args:
            list_widget (QListWidget): the list to update

        """
        item = list_widget.currentItem()
        if not item:
            return

        presets_manager.remove_prefixes(item.text())
        self._populate(list_widget, presets_manager.load_presets("prefixes"))
        self.prefixes_changed.emit(presets_manager.load_presets("prefixes"))

    def _on_add_suffix(self, field, list_widget):
        """Add a new suffix preset.

        Args:
            field (QLineEdit): input field
            list_widget (QListWidget): the list to update

        """
        value = field.text().strip()
        if not value:
            return

        existing = self._get_items(list_widget)
        if value in existing:
            self._show_warning(f"'{value}' already exists in suffixes.")
            return

        presets_manager.add_suffixes(value)
        self._populate(list_widget, presets_manager.load_presets("suffixes"))
        self.suffixes_changed.emit(presets_manager.load_presets("suffixes"))
        field.clear()

    def _on_remove_suffix(self, list_widget):
        """Remove selected suffix preset.

        Args:
            list_widget (QListWidget): the list to update

        """
        item = list_widget.currentItem()
        if not item:
            return

        presets_manager.remove_suffixes(item.text())
        self._populate(list_widget, presets_manager.load_presets("suffixes"))
        self.suffixes_changed.emit(presets_manager.load_presets("suffixes"))

    def _on_order_changed(self, list_widget, label):
        """Save the new order after drag and drop.

        Args:
            list_widget (QListWidget): the list that was reordered
            label (str): 'Prefixes' or 'Suffixes'

        """
        items = self._get_items(list_widget)
        if label == "Prefixes":
            presets_manager.save_prefixes(items)
            self.prefixes_changed.emit(items)
        else:
            presets_manager.save_suffixes(items)
            self.suffixes_changed(items)

    def _on_item_renamed(self, list_widget, label):
        """Save after an item is renamed by double_click.

        Args:
            list_widget (QListWidget): the list that was edited
            label (str): 'Prefixes' or 'Suffixes'

        """
        items = self._get_items(list_widget)
        if label == "Prefixes":
            presets_manager.save_prefixes(items)
            self.prefixes_changed.emit(items)
        else:
            presets_manager.save_suffixes(items)
            self.suffixes_changed.emit(items)

    def _on_reset(self):
        """Reset presets to defaults after confirmation."""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Reset to defaults",
            "This will overwrite your current presets.\nAre you sure?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        presets_manager.save_prefixes(constants.PREFIXES)
        presets_manager.save_suffixes(constants.SUFFIXES)
        self._load()
        self.prefixes_changed.emit(constants.PREFIXES)
        self.suffixes_changed.emit(constants.SUFFIXES)

    def _get_items(self, list_widget):
        """Get all items from a list widget.

        Args:
            list_widget (QListWidget): list

        Returns:
            list[str]: list of item texts

        """
        return [list_widget.item(i).text() for i in range(list_widget.count())]

    def _show_warning(self, message):
        """Show a warning message box.

        Args:
            message (str): warning message

        """
        QtWidgets.QMessageBox.warning(self, "Warning", message)
        log.warning(message)
