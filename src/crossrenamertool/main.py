import logging
import re

from crossrenamertool.core import constants
from crossrenamertool.maya import maya_api
from crossrenamertool.ui.maya import main_window as app_view

log = logging.getLogger(__name__)

_WINDOW = None

# ! Delete before publish
import importlib

importlib.reload(maya_api)
importlib.reload(app_view)
importlib.reload(constants)


class CrossRenamerToolController:
    """Controller for the module."""

    def __init__(self):
        self._view = None

    def rename_nodes(
        self,
        mode,
        base_name="",
        padding=constants.DEFAULT_PADDING,
        start=constants.DEFAULT_START,
        step=constants.DEFAULT_STEP,
    ):
        """Rename selected nodes.

        Args:
            mode (str): mode of selection
            base_name (str, optional): base name. Defaults to "".
            padding (int, optional): number of 0. Defaults to 3.
            start (int, optional): start number. Defaults to 1.
            step (int, optional): increment between each number. Defaults to 1.

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.rename_nodes(
            mode, base_name=base_name, padding=padding, start=start, step=step
        )

    def add_prefix(self, mode, prefix=""):
        """Add prefix to nodes.

        Args:
            mode (str): mode of selection
            prefix (str, optional): prefix. Defaults to "".

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.add_prefix(mode=mode, prefix=prefix)

    def add_suffix(self, mode, suffix=""):
        """Add suffix to nodes.

        Args:
            mode (str): mode of selection
            suffix (str, optional): suffix to add. Defaults to "".

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.add_suffix(mode, suffix)

    def remove_prefix(self, mode, prefix=""):
        """Remove prefix to nodes.

        Args:
            mode (str): mode of selection
            prefix (str, optional): prefix. Defaults to "".

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.remove_prefix(mode=mode, prefix=prefix)

    def remove_suffix(self, mode, suffix=""):
        """Remove suffix to nodes.

        Args:
            mode (str): mode of selection
            suffix (str, optional): suffix. Defaults to "".

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.remove_suffix(mode=mode, suffix=suffix)

    def search_replace(self, search_name, replace_name, case, regex):
        """Search and replace name in node.

        Args:
            search_name (str): name to find
            replace_name (str): new name to replace
            case (bool): case sensitive
            regex (bool): find by regex or not

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.search_replace(search_name, replace_name, case, regex)

    def update_preview_search_preview(self, search, replace, case, regex):
        return maya_api.update_preview_search_preview(search, replace, case, regex)

    def add_characters(self, mode, text, position, from_start):
        """Add characters to a text at a specific position.

        Args:
            mode (str): mode of selection
            text (str): characters to add
            position (int): position to insert
            from_start (bool): True if insert from start else False.

        Returns:
            dict[str, str]: dictionary of nodes

        """
        return maya_api.add_characters(mode, text, position, from_start)

    def remove_characters(self, mode, position, count, from_start):
        """Delete characters at given position in the node name.

        Args:
            mode (str): mode of selection
            position (int): start index of deletion
            count (int): number of characters to delete
            from_start (bool): True count from start else from end.

        Returns:
            dict[str, str]: dictionary of nodes

        """
        return maya_api.remove_characters(mode, position, count, from_start)

    def text_to_lowercase(self, mode):
        """Convert text to lowercase.

        Args:
            mode (str): mode of selection

        Returns:
            dict[str, str]: dictionary of nodes

        """
        return maya_api.text_to_lowercase(mode)

    def text_to_uppercase(self, mode):
        """Convert text to uppercase.

        Args:
            mode (str): mode of selection

        Returns:
            dict[str, str]: dictionary of nodes

        """
        return maya_api.text_to_uppercase(mode)

    def text_to_capitalize(self, mode):
        """Convert text to capitalize.

        Args:
            mode (str): mode of selection

        Returns:
            dict[str, str]: dictionary of nodes

        """
        return maya_api.text_to_capitalize(mode)

    def rename_children_from_parent(self, mode, padding=constants.DEFAULT_PADDING):

        return maya_api.rename_children_from_parent(mode, padding=padding)

    def get_duplicates(self):
        """Get duplicates nodes in the scene.

        Returns:
            list[str]: list of duplicates nodes

        """
        return maya_api.get_duplicates()

    def fix_duplicates(self, items):
        return maya_api.fix_duplicates(items=items)

    def auto_fix_duplicates(self):
        """Auto rename duplicates nodes.

        Returns:
            dict[str, str]: renamed nodes

        """
        return maya_api.auto_fix_duplicates()

    def select_item(self, index, datas):
        """Select the node by the duplicates table.

        Args:
            index (int): index in the table
            datas (dict[str, str]): duplicates node dictionary

        Returns:
            str: name of the selected node

        """
        return maya_api.select_item(index, datas)

    def swap_side(self, mode):
        """Swap side indicator in the node.

        Args:
            mode (str): selected mode

        Returns:
            str: new name swap

        """
        return maya_api.swap_side(mode=mode)

    def fix_shape_name(self):
        """Rename shapes to match their transform name.

        Returns:
            dict[str, str]: {old_name: new_name}

        """
        return maya_api.fix_shape_name()

    def set_view(self, view):
        """Attach a view instance to the controller.

        Args:
            view (CrossRenamerToolView): view instance that will be managed by the controller.

        """
        global _WINDOW
        self._view = view
        _WINDOW = self._view

    def delete_workspace_control(self, workspace_name: str) -> None:
        """Close and delete an existing Maya workspace control.

        Args:
            workspace_name (str): name of the workspace control to delete

        """
        maya_api.delete_workspace_control(workspace_name)

    def launch(self) -> None:
        """Launch the application by displaying the view."""
        if self._view is None:
            log.error("No view attached to controller")
            raise RuntimeError("Cannot launch: no view attached")

        self._view.launch_app()
        log.info("Cross Renamer Tool launched successfully")


def create_controller():
    """Create Cross Renamer Tool.

    Returns:
        return the controller.

    """
    controller = CrossRenamerToolController()
    controller.set_view(view=app_view.create_view(controller=controller))

    controller.launch()
    return controller
