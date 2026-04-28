import logging

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants
from crossrenamertool.ui.maya import container

log = logging.getLogger(__name__)

# ! Delete before publish
import importlib

importlib.reload(constants)
importlib.reload(container)


class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    """Main Window for the tool."""

    TITLE = "Cross Renamer Tool"
    OBJECT_NAME = "CrossRenamerToolMainWindow"

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.rename_txt = None
        self.padding = None
        self.start = None
        self.step = None
        self.prefix = None

        self._configure()
        self._create_gui()

    def _configure(self):
        """Configure the window."""
        self.setWindowTitle(f"{self.TITLE} v1.0.0")
        self.setObjectName(self.OBJECT_NAME)
        self.resize(300, 500)

    def _create_gui(self):
        """Create the gui."""

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QVBoxLayout(main_widget)

        mode_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(mode_layout)

        selected_mode = QtWidgets.QRadioButton("Selected")
        selected_mode.setChecked(True)
        mode_layout.addWidget(selected_mode, 2, 0)

        hierarchy_mode = QtWidgets.QRadioButton("Hierarchy")
        mode_layout.addWidget(hierarchy_mode, 2, 1)

        scene_mode = QtWidgets.QRadioButton("Scene")
        mode_layout.addWidget(scene_mode, 2, 2)

        self.mode_group = QtWidgets.QButtonGroup()
        self.mode_group.addButton(selected_mode, 0)
        self.mode_group.addButton(hierarchy_mode, 1)
        self.mode_group.addButton(scene_mode, 2)

        name_container = container.Container("Name", color_background=False)
        main_layout.addWidget(name_container)

        name_content_layout = QtWidgets.QVBoxLayout(name_container.contentWidget)

        name_group = QtWidgets.QGroupBox()
        name_content_layout.addWidget(name_group)

        name_layout = QtWidgets.QVBoxLayout()
        name_group.setLayout(name_layout)

        rename_layout = QtWidgets.QFormLayout()
        name_layout.addLayout(rename_layout)

        self.rename_txt = QtWidgets.QLineEdit()
        self.rename_txt.setPlaceholderText("New Name...")
        rename_layout.addRow("Rename", self.rename_txt)

        name_configuration_layout = QtWidgets.QHBoxLayout()
        name_layout.addLayout(name_configuration_layout)

        self.padding = QtWidgets.QSpinBox()
        self.padding.setRange(1, 10)
        self.padding.setValue(constants.DEFAULT_PADDING)
        padding_layout = self._create_horizontal_form_layout("Padding", self.padding)
        name_configuration_layout.addLayout(padding_layout)

        self.start = QtWidgets.QSpinBox()
        self.start.setRange(1, 10)
        self.start.setValue(constants.DEFAULT_START)
        start_layout = self._create_horizontal_form_layout("Start", self.start)
        name_configuration_layout.addLayout(start_layout)

        self.step = QtWidgets.QSpinBox()
        self.step.setRange(1, 100)
        self.step.setValue(constants.DEFAULT_STEP)
        step_layout = self._create_horizontal_form_layout("Step", self.step)
        name_configuration_layout.addLayout(step_layout)

        rename_btn = QtWidgets.QPushButton("Rename")
        name_layout.addWidget(rename_btn)

        prefix_suffix_group = QtWidgets.QGroupBox()
        name_content_layout.addWidget(prefix_suffix_group)

        prefix_suffix_layout = QtWidgets.QVBoxLayout()
        prefix_suffix_group.setLayout(prefix_suffix_layout)

        prefix_layout = QtWidgets.QHBoxLayout()
        prefix_suffix_layout.addLayout(prefix_layout)

        self.prefix = QtWidgets.QComboBox()
        self.prefix.setMinimumWidth(200)
        self.prefix.addItems(constants.PREFIXES)
        self.prefix.setEditable(True)
        self.prefix.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.prefix.setCurrentIndex(-1)
        self.prefix.lineEdit().setPlaceholderText("Left")

        prefix_widget_layout = self._create_horizontal_form_layout(
            "Prefix", self.prefix
        )
        prefix_layout.addLayout(prefix_widget_layout)

        prefix_btn = QtWidgets.QPushButton("Add")
        prefix_btn.setMaximumWidth(50)
        prefix_layout.addWidget(prefix_btn)

        suffix_layout = QtWidgets.QHBoxLayout()
        prefix_suffix_layout.addLayout(suffix_layout)

        self.suffix = QtWidgets.QComboBox()
        self.suffix.setMinimumWidth(200)
        self.suffix.addItems(constants.SUFFIXES)
        self.suffix.setEditable(True)
        self.suffix.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.suffix.setCurrentIndex(-1)
        self.suffix.lineEdit().setPlaceholderText("ctrl")

        suffix_widget_layout = self._create_horizontal_form_layout(
            "Suffix", self.suffix
        )
        suffix_layout.addLayout(suffix_widget_layout)

        suffix_btn = QtWidgets.QPushButton("Add")
        suffix_btn.setMaximumWidth(50)
        suffix_layout.addWidget(suffix_btn)

        search_replace_container = container.Container(
            "Search/Replace", color_background=False
        )
        main_layout.addWidget(search_replace_container)

        search_replace_content_layout = QtWidgets.QGridLayout(
            search_replace_container.contentWidget
        )

        search_label = QtWidgets.QLabel("Search")
        search_replace_content_layout.addWidget(search_label, 0, 0)

        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Text to search for...")
        search_replace_content_layout.addWidget(self.search, 0, 1, 1, 2)

        replace_label = QtWidgets.QLabel("Replace")
        search_replace_content_layout.addWidget(replace_label, 1, 0)

        self.replace = QtWidgets.QLineEdit()
        self.replace.setPlaceholderText("Text to be replaced...")
        search_replace_content_layout.addWidget(self.replace, 1, 1, 1, 2)

        search_replace_btn = QtWidgets.QPushButton("Add")
        search_replace_content_layout.addWidget(search_replace_btn, 3, 0, 1, 3)

        add_character_container = container.Container(
            "Add characters", color_background=False
        )
        main_layout.addWidget(add_character_container)

        add_character_content_layout = QtWidgets.QGridLayout(
            add_character_container.contentWidget
        )

        self.add_start_character = QtWidgets.QSpinBox()
        self.add_start_character.setSingleStep(1)
        self.add_start_character.setRange(0, 99)
        add_character_content_layout.addWidget(self.add_start_character, 0, 0)

        add_start_btn = QtWidgets.QPushButton("+")
        add_character_content_layout.addWidget(add_start_btn, 0, 1)

        self.text_to_add = QtWidgets.QLineEdit()
        self.text_to_add.setPlaceholderText("Text to add...")
        add_character_content_layout.addWidget(self.text_to_add, 0, 2)

        self.add_end_character = QtWidgets.QSpinBox()
        self.add_end_character.setSingleStep(1)
        self.add_end_character.setRange(0, 99)
        add_character_content_layout.addWidget(self.add_end_character, 0, 3)

        add_end_btn = QtWidgets.QPushButton("+")
        add_character_content_layout.addWidget(add_end_btn, 0, 4)

        convert_case_container = container.Container(
            "Convert case", color_background=False
        )
        main_layout.addWidget(convert_case_container)

        convert_case_content_layout = QtWidgets.QGridLayout(
            convert_case_container.contentWidget
        )

        lowercase_btn = QtWidgets.QPushButton("Lowercase")
        convert_case_content_layout.addWidget(lowercase_btn, 0, 0)

        uppercase_btn = QtWidgets.QPushButton("Uppercase")
        convert_case_content_layout.addWidget(uppercase_btn, 0, 1)

        capitalize_btn = QtWidgets.QPushButton("Capitalize")
        convert_case_content_layout.addWidget(capitalize_btn, 0, 2)

        rename_btn.clicked.connect(self._on_rename_btn_clicked)
        prefix_btn.clicked.connect(self._on_prefix_btn_clicked)
        suffix_btn.clicked.connect(self._on_suffix_btn_clicked)
        search_replace_btn.clicked.connect(self._on_search_replace_btn_clicked)
        add_start_btn.clicked.connect(self._on_add_start_btn_clicked)
        add_end_btn.clicked.connect(self._on_add_end_btn_clicked)
        lowercase_btn.clicked.connect(self._on_lowercase_btn_clicked)
        uppercase_btn.clicked.connect(self._on_uppercase_btn_clicked)
        capitalize_btn.clicked.connect(self._on_capitalize_btn_clicked)

    def _create_horizontal_form_layout(self, label, widget):
        """Create horizontal form layout.

        Args:
            label (str): text for the label
            widget (QtWidget): widget to add

        Returns:
            QtWidget.QHBoxLayout: horizontal layout

        """
        row = QtWidgets.QHBoxLayout()
        row.addWidget(QtWidgets.QLabel(label))
        row.addWidget(widget)
        return row

    def get_current_mode(self):
        ids = {0: "Selected", 1: "Hierarchy", 2: "Scene"}
        return ids[self.mode_group.checkedId()]

    def _on_rename_btn_clicked(self):
        """Rename the selected nodes."""
        name = self.rename_txt.text()
        padding = self.padding.value()
        start = self.start.value()
        step = self.step.value()
        mode = self.get_current_mode()
        self.controller.rename_nodes(mode, name, padding, start, step)

    def _on_prefix_btn_clicked(self):
        """Add prefix to nodes."""
        prefix = self.prefix.currentText()
        mode = self.get_current_mode()
        self.controller.add_prefix(mode, prefix)

    def _on_suffix_btn_clicked(self):
        """Add suffix to nodes."""
        suffix: str = self.suffix.currentText()
        mode = self.get_current_mode()
        self.controller.add_suffix(mode, suffix)

    def _on_search_replace_btn_clicked(self):
        search_text = self.search.text()
        replace_text = self.replace.text()
        mode = self.get_current_mode()

        self.controller.search_replace(mode, search_text, replace_text)

    def _on_add_start_btn_clicked(self):
        text = self.text_to_add.text()
        position = self.add_start_character.value()
        mode = self.get_current_mode()

        self.controller.add_characters(
            mode=mode, text=text, position=position, from_start=True
        )

    def _on_add_end_btn_clicked(self):
        text = self.text_to_add.text()
        position = self.add_end_character.value()
        mode = self.get_current_mode()

        self.controller.add_characters(
            mode=mode, text=text, position=position, from_start=False
        )

    def _on_lowercase_btn_clicked(self):
        mode = self.get_current_mode()
        self.controller.text_to_lowercase(mode)

    def _on_uppercase_btn_clicked(self):
        mode = self.get_current_mode()
        self.controller.text_to_uppercase(mode)

    def _on_capitalize_btn_clicked(self):
        mode = self.get_current_mode()
        self.controller.text_to_capitalize(mode)

    def launch_app(self):
        """Launch the application."""
        self.show(dockable=True)


def create_view(controller):
    """Create the view of the module.

    Args:
        controller (CrossRenamerToolController): controller of the module.

    """
    workspace_name = MainWindow.OBJECT_NAME + "WorkspaceControl"
    controller.delete_workspace_control(workspace_name)

    try:
        view = MainWindow(controller=controller)
        log.info("MainWindow created successfully")
        return view
    except Exception as e:
        log.error(f"Failed to create MainWindow: {e}")
        controller.delete_workspace_control(workspace_name)
        raise
