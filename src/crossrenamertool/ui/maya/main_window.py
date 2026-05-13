import logging

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide6 import QtCore, QtGui, QtWidgets

from crossrenamertool.core import constants
from crossrenamertool.ui.maya.widgets import (
    case_widget,
    insert_remove_widget,
    prefix_suffix_widget,
    rename_widget,
    search_replace_widget,
    utils_widget,
)

log = logging.getLogger(__name__)

# ! Delete before publish
import importlib

importlib.reload(constants)
importlib.reload(rename_widget)
importlib.reload(prefix_suffix_widget)
importlib.reload(search_replace_widget)
importlib.reload(insert_remove_widget)
importlib.reload(case_widget)
importlib.reload(utils_widget)


class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    """Main Window for the tool."""

    TITLE = "Cross Renamer Tool"
    OBJECT_NAME = "CrossRenamerToolMainWindow"
    PAGES = [
        "Rename",
        "Prefix/Suffix",
        "Search/Replace",
        "Insert/Remove",
        "Convert Case",
        "Utils",
    ]
    UTILS_PAGE_INDEX = 5

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.rename_page = rename_widget.RenamePage()
        self.prefix_suffix_page = prefix_suffix_widget.PrefixSuffixPage()
        self.search_replace_page = search_replace_widget.SearchReplacePage()
        self.insert_remove_page = insert_remove_widget.InsertRemovePage()
        self.case_page = case_widget.CasePage()
        self.utils_page = utils_widget.UtilsPage()
        self.datas = {}

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

        # Mode layout
        mode_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(mode_layout)
        mode_label = QtWidgets.QLabel("Apply on :")
        mode_layout.addWidget(mode_label)
        selected_mode = QtWidgets.QRadioButton("Selected")
        selected_mode.setChecked(True)
        mode_layout.addWidget(selected_mode)
        hierarchy_mode = QtWidgets.QRadioButton("Hierarchy")
        mode_layout.addWidget(hierarchy_mode)
        scene_mode = QtWidgets.QRadioButton("Scene")
        mode_layout.addWidget(scene_mode)
        self.mode_group = QtWidgets.QButtonGroup()
        self.mode_group.addButton(selected_mode, 0)
        self.mode_group.addButton(hierarchy_mode, 1)
        self.mode_group.addButton(scene_mode, 2)
        mode_layout.addStretch()
        main_layout.addLayout(mode_layout)

        # Navigation bar
        navigation_row = QtWidgets.QHBoxLayout()
        navigation_row.setSpacing(2)
        self.navigation_group = QtWidgets.QButtonGroup()

        for index, label in enumerate(self.PAGES):
            button = QtWidgets.QPushButton(label)
            button.setCheckable(True)
            button.setFixedHeight(28)
            self.navigation_group.addButton(button, index)
            navigation_row.addWidget(button)

        self.navigation_group.button(0).setChecked(True)
        self.navigation_group.idClicked.connect(self._on_navigation_clicked)
        main_layout.addLayout(navigation_row)

        # Pages
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.rename_page)
        self.stack.addWidget(self.prefix_suffix_page)
        self.stack.addWidget(self.search_replace_page)
        self.stack.addWidget(self.insert_remove_page)
        self.stack.addWidget(self.case_page)
        self.stack.addWidget(self.utils_page)
        main_layout.addWidget(self.stack)

        self.rename_page.request_rename.connect(self.rename_nodes)
        self.prefix_suffix_page.request_prefix.connect(self.add_prefix)
        self.prefix_suffix_page.request_suffix.connect(self.add_suffix)
        self.search_replace_page.request_search_replace.connect(self.search_replace)
        self.insert_remove_page.request_start_insert.connect(
            self.insert_start_characters
        )
        self.insert_remove_page.request_end_insert.connect(self.insert_end_characters)
        self.insert_remove_page.request_start_remove.connect(
            self.remove_start_characters
        )
        self.insert_remove_page.request_end_remove.connect(self.remove_end_characters)
        self.case_page.request_lowercase.connect(self.text_to_lowercase)
        self.case_page.request_uppercase.connect(self.text_to_uppercase)
        self.case_page.request_capitalize.connect(self.text_to_capitalize)
        self.utils_page.request_rename_children_from_parent.connect(
            self.rename_children_from_parent
        )

        self.utils_page.request_fix.connect(self.fix_duplicates)
        self.utils_page.request_auto_fix.connect(self.auto_fix_duplicates)
        self.utils_page.request_select_item.connect(self.select_item)
        self.utils_page.request_refresh.connect(self.refresh)
        self.utils_page.request_swap.connect(self.swap)

    def refresh(self):
        self.datas = self.controller.get_duplicates()
        self.utils_page.ingest_list(self.datas)

    def _on_navigation_clicked(self, index):
        """Change to page display.

        Args:
            index (int): index of the page

        """
        self.stack.setCurrentIndex(index)

        if index == self.UTILS_PAGE_INDEX:
            self.datas = self.controller.get_duplicates()
            self.utils_page.ingest_list(self.datas)

    def get_current_mode(self):
        """Get current mode.

        Returns:
            dict[int, str]: selected mode

        """
        ids = {0: "Selected", 1: "Hierarchy", 2: "Scene"}
        return ids[self.mode_group.checkedId()]

    def rename_nodes(self, name, padding, start, step):
        """Rename selected nodes.

        Args:
            name (str, optional): base name. Defaults to "".
            padding (int, optional): number of 0. Defaults to 3.
            start (int, optional): start number. Defaults to 1.
            step (int, optional): increment between each number. Defaults to 1.

        """
        mode = self.get_current_mode()
        self.controller.rename_nodes(mode, name, padding, start, step)

    def add_prefix(self, prefix):
        """Add prefix to nodes.

        Args:
            prefix (str, optional): prefix. Defaults to "".

        """
        mode = self.get_current_mode()
        self.controller.add_prefix(mode, prefix)

    def add_suffix(self, suffix):
        """Add suffix to nodes.

        Args:
            suffix (str, optional): suffix to add. Defaults to "".

        """
        mode = self.get_current_mode()
        self.controller.add_suffix(mode, suffix)

    def search_replace(self, search_text, replace_text, case):
        """Search and replace name in node.

        Args:
            search_text (str): name to find
            replace_text (str): new name to replace
            case (bool): case sensitive

        """
        mode = self.get_current_mode()
        self.controller.search_replace(mode, search_text, replace_text, case)

    def insert_start_characters(self, text, position):
        """Add characters to a text at a specific position by the start.

        Args:
            text (str): characters to add
            position (int): position to insert

        """
        mode = self.get_current_mode()

        self.controller.add_characters(
            mode=mode, text=text, position=position, from_start=True
        )

    def insert_end_characters(self, text, position):
        """Add characters to a text at a specific position by the end.

        Args:
            text (str): characters to add
            position (int): position to insert

        """
        mode = self.get_current_mode()

        self.controller.add_characters(
            mode=mode, text=text, position=position, from_start=False
        )

    def remove_start_characters(self, count, position):
        """Remove characters to a text at a specific position by the start.

        Args:
            count (int): number of characters to remove
            position (int): position to remove

        """
        mode = self.get_current_mode()

        self.controller.remove_characters(
            mode=mode, position=position, count=count, from_start=True
        )

    def remove_end_characters(self, count, position):
        """Remove characters to a text at a specific position by the end.

        Args:
            count (int): number of characters to remove
            position (int): position to remove

        """
        mode = self.get_current_mode()

        self.controller.remove_characters(
            mode=mode, position=position, count=count, from_start=False
        )

    def text_to_lowercase(self):
        """Convert text to lowercase."""
        mode = self.get_current_mode()
        self.controller.text_to_lowercase(mode)

    def text_to_uppercase(self):
        """Convert text to uppercase."""
        mode = self.get_current_mode()
        self.controller.text_to_uppercase(mode)

    def text_to_capitalize(self):
        """Convert text to capitalize."""
        mode = self.get_current_mode()
        self.controller.text_to_capitalize(mode)

    def rename_children_from_parent(self, padding):
        mode = self.get_current_mode()
        self.controller.rename_children_from_parent(mode, padding)

    def auto_fix_duplicates(self):
        self.controller.auto_fix_duplicates()

    def fix_duplicates(self, items):
        self.controller.fix_duplicates(items)

    def select_item(self, index):
        self.controller.select_item(index, self.datas)

    def swap(self):
        mode = self.get_current_mode()
        self.controller.swap_side(mode)

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
