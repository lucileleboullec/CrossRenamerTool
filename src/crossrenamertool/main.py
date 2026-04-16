from crossrenamertool.maya import maya_api
from crossrenamertool.ui.maya import main_window as app_view

_WINDOW = None

# ! Delete before publish
import importlib

importlib.reload(maya_api)
importlib.reload(app_view)


class CrossRenamerToolController:
    """Controller for the module."""

    def __init__(self):
        self._view = None

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
            print("No view attached to controller")
            raise RuntimeError("Cannot launch: no view attached")

        self._view.launch_app()
        print("Cross Renamer Tool launched successfully")


def create_controller():
    """Create Cross Renamer Tool.

    Returns:
        return the controller.

    """
    controller = CrossRenamerToolController()
    controller.set_view(view=app_view.create_view(controller=controller))

    controller.launch()
    return controller
