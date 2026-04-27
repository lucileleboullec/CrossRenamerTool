"""Maya adapter."""

import uuid

from crossrenamertool.core import renamer, constants
import maya.cmds as cmds

import logging

log = logging.getLogger(__name__)

# ! Delete before publish
import importlib

importlib.reload(renamer)
importlib.reload(constants)


def get_selection():
    """Get the current selection.

    Returns:
        list: list of selected node names

    """
    return cmds.ls(sl=True) or []


def get_hierarchy():
    selected = get_selection()
    if not selected:
        log.warning("Select at least 1 node.")
        return []
    nodes = (
        cmds.listRelatives(
            selected, allDescendents=True, fullPath=False, type="transform"
        )
        or []
    )
    nodes = selected + nodes

    return nodes


def get_scene_objects():
    nodes = cmds.ls(transforms=True) or []

    return [node for node in nodes if node not in constants.DEFAULT_CAMS]


def _apply_rename(node, new_name, old_name=""):
    """Apply rename.

    Args:
        node (str): current node name
        new_name (str): desired new name
        old_name (str): original name

    Returns:
        str: actual name applied by Maya

    """
    actual_name = cmds.rename(node, new_name)
    if not old_name:
        old_name = node

    if actual_name != new_name:
        log.warning(
            f"{old_name} renamed to {actual_name} instead of {new_name} (name conflict)."
        )
    else:
        log.info(f"{old_name} -> {actual_name}")

    return actual_name


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
        return None

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
            continue
        new_name = renamer.renaming(base_name, index, padding)
        renamed[old_node] = _apply_rename(node, new_name, old_node)

    return renamed


def add_prefix(prefix):
    """Add prefix to nodes.

    Args:
        prefix (str): prefix

    Returns:
        dict[str, str]: renamed nodes

    """
    nodes = get_selection()

    if not nodes:
        log.warning("Select at least 1 node.")
        return None

    renamed = {}
    for node in nodes:
        if not cmds.objExists(node):
            log.error(f"The node {node} doesn't exist.")
            continue

        new_name = renamer.add_prefix(base_name=node, prefix=prefix)
        renamed[node] = _apply_rename(node, new_name)

    return renamed


def add_suffix(suffix):
    """Add suffix to nodes.

    Args:
        suffix (str): suffix to add

    Returns:
        dict[str, str]: renamed nodes

    """
    nodes = get_selection()

    if not nodes:
        log.warning("Select at least 1 node.")
        return None

    renamed = {}
    for node in nodes:
        if not cmds.objExists(node):
            log.error(f"The node {node} doesn't exist.")
            continue

        new_name = renamer.add_suffix(base_name=node, suffix=suffix)
        renamed[node] = _apply_rename(node, new_name)

    return renamed


def search_replace(mode, search_name, replace_name) -> dict[str, str]:
    """Search and replace name in node.

    Args:
        node (str): node selected
        search_name (str): name to find
        replace_name (str): new name to replace

    Returns:
        dict[str, str]: renamed nodes

    """
    if mode == "Selected":
        nodes = get_selection()

    elif mode == "Hierarchy":
        nodes = get_hierarchy()

    elif mode == "Scene":
        nodes = get_scene_objects()

    else:
        log.error(f"Unknown mode: {mode}")
        return []

    renamed = {}
    for node in nodes:
        if not cmds.objExists(node):
            log.error(f"The node {node} doesn't exist.")
            continue

        new_name = renamer.search_replace(node, search_name, replace_name)
        if node != new_name:
            renamed[node] = _apply_rename(node, new_name)
        else:
            renamed[node] = node

    return renamed


def delete_workspace_control(workspace_name: str) -> None:
    """Close and delete an existing Maya workspace control.

    Args:
        workspace_name (str): name of the workspace control to delete

    """
    if cmds.workspaceControl(workspace_name, exists=True):
        cmds.workspaceControl(workspace_name, edit=True, close=True)
        cmds.deleteUI(workspace_name, control=True)
