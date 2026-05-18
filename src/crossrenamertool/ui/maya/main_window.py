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
    selection_mode_widget,
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
importlib.reload(selection_mode_widget)


class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    """Main Window for the tool."""

    TITLE = "Cross Renamer"
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
        self.mode_bar = selection_mode_widget.SelectionModeBar()
        self.datas = {}

        self._configure()
        self._create_gui()

    def _configure(self):
        """Configure the window."""
        self.setWindowTitle(f"{self.TITLE}")
        self.setObjectName(self.OBJECT_NAME)
        self.resize(500, 600)

    def _create_gui(self):
        """Create the gui."""
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QtWidgets.QWidget(self)
        header.setFixedHeight(44)
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(12, 0, 8, 0)

        title = QtWidgets.QLabel(self.TITLE.upper())
        header_layout.addWidget(title)
        header_layout.addStretch()

        about_btn = QtWidgets.QPushButton("?")
        about_btn.setFixedSize(24, 24)
        about_btn.setToolTip("About")
        # about_btn.clicked.connect(self._show_about)
        header_layout.addWidget(about_btn)

        main_layout.addWidget(header)

        # Mode layout
        mode_wrapper = QtWidgets.QWidget()
        mode_layout = QtWidgets.QHBoxLayout(mode_wrapper)
        mode_layout.setContentsMargins(10, 6, 10, 6)

        mode_label = QtWidgets.QLabel("Apply on :")
        mode_label.setFixedWidth(60)
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_bar)

        main_layout.addWidget(mode_wrapper)

        # Navigation bar
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tabs.addTab(self.rename_page, "Rename")
        self.tabs.addTab(self.prefix_suffix_page, "Prefix / Suffix")
        self.tabs.addTab(self.search_replace_page, "Search & Replace")
        self.tabs.addTab(self.insert_remove_page, "Insert / Remove")
        self.tabs.addTab(self.case_page, "Case")
        self.tabs.addTab(self.utils_page, "Utilities")

        main_layout.addWidget(self.tabs)

        self.rename_page.request_rename.connect(self.rename_nodes)
        self.prefix_suffix_page.request_prefix.connect(self.add_prefix)
        self.prefix_suffix_page.request_suffix.connect(self.add_suffix)
        self.prefix_suffix_page.request_remove_prefix.connect(self.remove_prefix)
        self.prefix_suffix_page.request_remove_suffix.connect(self.remove_suffix)

        self.search_replace_page.request_search_replace.connect(self.search_replace)
        self.search_replace_page.request_preview_search_replace.connect(
            self.update_preview_search_preview
        )
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
        self.utils_page.request_fix_shape_name.connect(self.fix_shape_name)

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

    def rename_nodes(self, name, padding, start, step):
        """Rename selected nodes.

        Args:
            name (str, optional): base name. Defaults to "".
            padding (int, optional): number of 0. Defaults to 3.
            start (int, optional): start number. Defaults to 1.
            step (int, optional): increment between each number. Defaults to 1.

        """
        self.controller.rename_nodes(self.mode_bar.mode, name, padding, start, step)

    def add_prefix(self, prefix):
        """Add prefix to nodes.

        Args:
            prefix (str, optional): prefix. Defaults to "".

        """
        self.controller.add_prefix(self.mode_bar.mode, prefix)

    def add_suffix(self, suffix):
        """Add suffix to nodes.

        Args:
            suffix (str, optional): suffix to add. Defaults to "".

        """
        self.controller.add_suffix(self.mode_bar.mode, suffix)

    def remove_prefix(self, prefix):
        """Remove prefix to nodes.

        Args:
            prefix (str, optional): prefix. Defaults to "".

        """
        self.controller.remove_prefix(self.mode_bar.mode, prefix)

    def remove_suffix(self, suffix):
        """Remove suffix to nodes.

        Args:
            suffix (str, optional): suffix. Defaults to "".

        """
        self.controller.remove_suffix(self.mode_bar.mode, suffix)

    def search_replace(self, search_text, replace_text, case, regex):
        """Search and replace name in node.

        Args:
            search_text (str): name to find
            replace_text (str): new name to replace
            case (bool): case sensitive
            regex (bool): find by regex or not

        """
        self.controller.search_replace(search_text, replace_text, case, regex)

    def update_preview_search_preview(self, search, replace, case, regex):
        texts = self.controller.update_preview_search_preview(
            search, replace, case, regex
        )
        self.search_replace_page.preview_label.setText(texts)

    def insert_start_characters(self, text, position):
        """Add characters to a text at a specific position by the start.

        Args:
            text (str): characters to add
            position (int): position to insert

        """
        self.controller.add_characters(
            mode=self.mode_bar.mode, text=text, position=position, from_start=True
        )

    def insert_end_characters(self, text, position):
        """Add characters to a text at a specific position by the end.

        Args:
            text (str): characters to add
            position (int): position to insert

        """
        self.controller.add_characters(
            mode=self.mode_bar.mode, text=text, position=position, from_start=False
        )

    def remove_start_characters(self, count, position):
        """Remove characters to a text at a specific position by the start.

        Args:
            count (int): number of characters to remove
            position (int): position to remove

        """
        self.controller.remove_characters(
            mode=self.mode_bar.mode, position=position, count=count, from_start=True
        )

    def remove_end_characters(self, count, position):
        """Remove characters to a text at a specific position by the end.

        Args:
            count (int): number of characters to remove
            position (int): position to remove

        """
        self.controller.remove_characters(
            mode=self.mode_bar.mode, position=position, count=count, from_start=False
        )

    def text_to_lowercase(self):
        """Convert text to lowercase."""
        self.controller.text_to_lowercase(self.mode_bar.mode)

    def text_to_uppercase(self):
        """Convert text to uppercase."""
        self.controller.text_to_uppercase(self.mode_bar.mode)

    def text_to_capitalize(self):
        """Convert text to capitalize."""
        self.controller.text_to_capitalize(self.mode_bar.mode)

    def rename_children_from_parent(self, padding):
        self.controller.rename_children_from_parent(self.mode_bar.mode, padding)

    def auto_fix_duplicates(self):
        self.controller.auto_fix_duplicates()

    def fix_duplicates(self, items):
        self.controller.fix_duplicates(items)

    def select_item(self, index):
        self.controller.select_item(index, self.datas)

    def swap(self):
        self.controller.swap_side(self.mode_bar.mode)

    def fix_shape_name(self):
        self.controller.fix_shape_name()

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
