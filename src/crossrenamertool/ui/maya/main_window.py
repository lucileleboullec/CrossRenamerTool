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
        self.setWindowTitle(self.TITLE + "v1.0.0")
        self.setObjectName(self.OBJECT_NAME)
        self.resize(300, 500)

    def _create_gui(self):
        """Create the gui."""

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QVBoxLayout(main_widget)

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

        search_replace_content_layout = QtWidgets.QVBoxLayout(
            search_replace_container.contentWidget
        )

        search_replace_btn = QtWidgets.QPushButton("Add")
        search_replace_content_layout.addWidget(search_replace_btn)

        rename_btn.clicked.connect(self._on_rename_btn_clicked)
        prefix_btn.clicked.connect(self._on_prefix_btn_clicked)
        suffix_btn.clicked.connect(self._on_suffix_btn_clicked)
        search_replace_btn.clicked.connect(self._on_search_replace_btn_clicked)

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

    def _on_rename_btn_clicked(self):
        """Rename the selected nodes."""
        name = self.rename_txt.text()
        padding = self.padding.value()
        start = self.start.value()
        step = self.step.value()
        self.controller.rename_nodes(name, padding, start, step)

    def _on_prefix_btn_clicked(self):
        """Add prefix to nodes."""
        prefix = self.prefix.currentText()
        self.controller.add_prefix(prefix)

    def _on_suffix_btn_clicked(self):
        """Add suffix to nodes."""
        suffix: str = self.suffix.currentText()
        self.controller.add_suffix(suffix)

    def _on_search_replace_btn_clicked(self):
        self.controller.search_replace("hierarchy", "Cube", "base")

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
