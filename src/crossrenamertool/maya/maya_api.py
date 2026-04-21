"""Maya adapter."""

import uuid

from crossrenamertool.core import renamer
import maya.cmds as cmds

import logging

log = logging.getLogger(__name__)

# ! Delete before publish
import importlib

importlib.reload(renamer)


def get_selection():
    """Get the selection.

    Returns:
        list: list of the selection

    """
    return cmds.ls(sl=True)


def rename_nodes(base_name, padding, start, step):
    """Rename nodes with padding, step and start.

    Args:
        base_name (str): base name
        padding (int): number of 0
        start (int): start number
        step (int): increment between each number

    Returns:
        dict[str, str]: renamed nodes

    """
    nodes = get_selection()

    renamed = {}
    if not nodes:
        log.warning("Select at least 1 node.")

    # Range of index with step
    numbers = range(start, start + len(nodes) * step, step)

    # Rename to temp name to avoid name conflict
    temp_names = []
    for node in nodes:
        temp = f"__tmp_{uuid.uuid4().hex[:8]}__"
        temp_name = cmds.rename(node, temp)
        temp_names.append(temp_name)

    for node, index, old_node in zip(temp_names, numbers, nodes):
        if not cmds.objExists(node):
            log.error(f"The node {node} doesn't exist.")
        new_name = renamer.renaming(base_name, index, padding)
        actual_name = cmds.rename(node, new_name)

        if actual_name != new_name:
            log.warning(
                f"{old_node} renamed to {actual_name} instead of {new_name} (name conflict)."
            )
        else:
            log.info(f"{old_node} -> {actual_name}")

        renamed[old_node] = actual_name

    return renamed


def delete_workspace_control(workspace_name: str) -> None:
    """Close and delete an existing Maya workspace control.

    Args:
        workspace_name (str): name of the workspace control to delete

    """
    if cmds.workspaceControl(workspace_name, exists=True):
        cmds.workspaceControl(workspace_name, edit=True, close=True)
        cmds.deleteUI(workspace_name, control=True)
