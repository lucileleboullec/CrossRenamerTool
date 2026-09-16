import logging

from PySide6 import QtCore, QtWidgets

from crossrenamertool.core import presets
from crossrenamertool.ui.maya.widgets import preset_combobox

log = logging.getLogger(__name__)


class PrefixSuffixPage(QtWidgets.QWidget):
    """Widget for prefix and suffix options."""

    TITLE = "Prefix/Suffix"

    request_prefix = QtCore.Signal(str)
    request_suffix = QtCore.Signal(str)
    request_remove_prefix = QtCore.Signal(str)
    request_remove_suffix = QtCore.Signal(str)
    request_manage = QtCore.Signal(str, str)

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

        manage_btn = QtWidgets.QPushButton("Manage Presets...")
        manage_btn.setFixedWidth(120)
        manage_btn.clicked.connect(self._on_open_manager)
        main_layout.addWidget(manage_btn, alignment=QtCore.Qt.AlignRight)

        prefix_group = QtWidgets.QGroupBox("Prefix")
        prefix_layout = QtWidgets.QVBoxLayout(prefix_group)
        prefix_layout.setSpacing(6)
        main_layout.addWidget(prefix_group)

        # Prefix
        prefix_row = QtWidgets.QHBoxLayout()
        self.prefix = preset_combobox.PresetComboBox()
        self.prefix.addItems(presets.load_presets("prefixes"))
        self.prefix.setToolTip(
            "<p>Prefix to add before the node name.</p><p style='color: #95a5a6;'>Example: 'CTRL' ➞ CTRL_arm_L</p>"
        )
        self.prefix.setEditable(True)
        self.prefix.setCurrentIndex(-1)
        self.prefix.lineEdit().setPlaceholderText("e.g. geo")
        self.prefix.setFixedHeight(30)
        self.prefix.request_save.connect(lambda value: self._on_save_preset("prefixes", value, self.prefix))
        self.prefix.request_remove.connect(lambda value: self._on_remove_preset("prefixes", value, self.prefix))
        self.prefix.request_manage.connect(self._on_open_manager)
        prefix_row.addWidget(self.prefix)

        add_prefix_btn = QtWidgets.QPushButton("Add Prefix")
        add_prefix_btn.setToolTip(
            "<p>Add the prefix to all selected nodes.</p><p style='color: #95a5a6;'>Example: arm_L ➞ CTRL_arm_L</p>"
        )
        add_prefix_btn.setObjectName("primary")
        add_prefix_btn.setFixedWidth(90)
        add_prefix_btn.clicked.connect(self._on_add_prefix)
        prefix_row.addWidget(add_prefix_btn)
        prefix_layout.addLayout(prefix_row)

        # Suffix
        suffix_group = QtWidgets.QGroupBox("Suffix")
        suffix_layout = QtWidgets.QVBoxLayout(suffix_group)
        suffix_layout.setSpacing(6)
        main_layout.addWidget(suffix_group)

        suffix_row = QtWidgets.QHBoxLayout()
        self.suffix = preset_combobox.PresetComboBox()
        self.suffix.setToolTip(
            "<p>Suffix to add after the node name.</p><p style='color: #95a5a6;'>Example: 'geo' ➞ arm_L_geo</p>"
        )
        self.suffix.addItems(presets.load_presets("suffixes"))
        self.suffix.setEditable(True)
        self.suffix.setCurrentIndex(-1)
        self.suffix.lineEdit().setPlaceholderText("e.g. GEO")
        self.suffix.setFixedHeight(30)
        self.suffix.request_save.connect(lambda value: self._on_save_preset("suffixes", value, self.suffix))
        self.suffix.request_remove.connect(lambda value: self._on_remove_preset("suffixes", value, self.suffix))
        self.suffix.request_manage.connect(self._on_open_manager)
        suffix_row.addWidget(self.suffix)

        add_suffix_btn = QtWidgets.QPushButton("Add Suffix")
        add_suffix_btn.setToolTip(
            "<p>Add the suffix to all selected nodes.</p><p style='color: #95a5a6;'>Example: arm_L ➞ arm_L_geo</p>"
        )
        add_suffix_btn.setObjectName("primary")
        add_suffix_btn.setFixedWidth(90)
        add_suffix_btn.clicked.connect(self._on_add_suffix)
        suffix_row.addWidget(add_suffix_btn)
        suffix_layout.addLayout(suffix_row)

        remove_group = QtWidgets.QGroupBox("Remove")
        remove_layout = QtWidgets.QHBoxLayout(remove_group)
        main_layout.addWidget(remove_group)

        remove_prefix_btn = QtWidgets.QPushButton("Remove Prefix")
        remove_prefix_btn.setToolTip(
            "<p>Remove the prefix added to the text field to all selected nodes.</p><p style='color: #95a5a6;'>Example: CTRL ➞ arm_L</p>"
        )
        remove_prefix_btn.setObjectName("danger")
        remove_prefix_btn.clicked.connect(self._on_remove_prefix)
        remove_layout.addWidget(remove_prefix_btn)

        remove_suffix_btn = QtWidgets.QPushButton("Remove Suffix")
        remove_suffix_btn.setToolTip(
            "<p>Remove the suffix added to the text field to all selected nodes.</p><p style='color: #95a5a6;'>Example: geo ➞ arm_L</p>"
        )
        remove_suffix_btn.setObjectName("danger")
        remove_suffix_btn.clicked.connect(self._on_remove_suffix)
        remove_layout.addWidget(remove_suffix_btn)

        main_layout.addStretch()

    def _load_prefix_presets(self) -> None:
        """Load prefix presets into the combobox."""
        self.prefix.clear()
        self.prefix.addItems(presets.load_presets("prefixes"))
        self.prefix.setCurrentIndex(-1)

    def _load_suffix_presets(self) -> None:
        """Load suffix presets into the combobox."""
        self.suffix.clear()
        self.suffix.addItems(presets.load_presets("suffixes"))
        self.suffix.setCurrentIndex(-1)

    def _on_add_prefix(self) -> None:
        """Add prefix to the node name."""
        prefix = self.prefix.currentText()
        if not prefix:
            return
        self.request_prefix.emit(prefix)

    def _on_add_suffix(self) -> None:
        """Add suffix to the node name."""
        suffix = self.suffix.currentText()
        if not suffix:
            return
        self.request_suffix.emit(suffix)

    def _on_remove_prefix(self) -> None:
        """Remove selected prefix on the selected object."""
        prefix = self.prefix.currentText().strip()
        if not prefix:
            return
        self.request_remove_prefix.emit(prefix)

    def _on_remove_suffix(self) -> None:
        """Remove selected suffix on the selected object."""
        suffix = self.suffix.currentText()
        if not suffix:
            return
        self.request_remove_suffix.emit(suffix)

    def _on_save_preset(self, preset_type, value, combo):
        """Save a value as preset and reload the combobox.

        Args:
            preset_type (str): "prefixes" or "suffixes"
            value (str): value to save
            combo (PresetComboBox): combobox to reload

        """
        existing = presets.load_presets(preset_type)
        if value in existing:
            QtWidgets.QMessageBox.information(self, "Already exists", f"'{value}' is already in the {preset_type}.")
            return

        presets.add_prefixes(value)
        combo.reload(presets.load_presets(preset_type))

    def _on_remove_preset(self, preset_type, value, combo):
        """Remove a value from presets and reload the combobox.

        Args:
            preset_type (str): "prefixes" or "suffixes"
            value (str): value to remove
            combo (PresetComboBox): combobox to reload

        """
        existing = presets.load_presets(preset_type)
        if value in existing:
            QtWidgets.QMessageBox.warning(self, "Not found", f"'{value}' is not in the {preset_type} presets.")
            return

        presets.remove_preset(preset_type, value)
        combo.reload(presets.load_presets(preset_type))

    def _on_open_manager(self):
        """Open the preset manager dialog."""
        self.request_manage.emit(self.prefix.reload, self.suffix.reload)
