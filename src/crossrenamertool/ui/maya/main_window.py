from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide6 import QtCore, QtGui, QtWidgets


class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    """Main Window for the tool."""

    TITLE = "Cross Renamer Tool"
    OBJECT_NAME = "CrossRenamerToolMainWindow"

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self._configure()
        self._create_gui()

    def _configure(self):
        """Configure the window."""
        self.setWindowTitle(self.TITLE)
        self.setObjectName(self.OBJECT_NAME)
        self.resize(300, 500)

    def _create_gui(self):
        """Create the gui."""

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QVBoxLayout(main_widget)

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
        print("MainWindow created successfully")
        return view
    except Exception as e:
        print(f"Failed to create MainWindow: {e}")
        controller.delete_workspace_control(workspace_name)
        raise
