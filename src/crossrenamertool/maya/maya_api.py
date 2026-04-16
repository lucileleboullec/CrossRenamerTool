"""Maya adapter."""

import maya.cmds as cmds


def delete_workspace_control(workspace_name: str) -> None:
    """Close and delete an existing Maya workspace control.

    Args:
        workspace_name (str): name of the workspace control to delete

    """
    if cmds.workspaceControl(workspace_name, exists=True):
        cmds.workspaceControl(workspace_name, edit=True, close=True)
        cmds.deleteUI(workspace_name, control=True)
