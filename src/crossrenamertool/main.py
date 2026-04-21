import logging

from crossrenamertool.maya import maya_api
from crossrenamertool.ui.maya import main_window as app_view

log = logging.getLogger(__name__)

_WINDOW = None

# ! Delete before publish
import importlib

importlib.reload(maya_api)
importlib.reload(app_view)


class CrossRenamerToolController:
    """Controller for the module."""

    def __init__(self):
        self._view = None

    def rename_nodes(self, base_name="", padding=3, start=1, step=1):
        """Rename selected nodes.

        Args:
            base_name (str, optional): base name. Defaults to "".
            padding (int, optional): number of 0. Defaults to 3.
            start (int, optional): start number. Defaults to 1.
            step (int, optional): increment between each number. Defaults to 1.

        """
        maya_api.rename_nodes(
            base_name=base_name, padding=padding, start=start, step=step
        )

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
