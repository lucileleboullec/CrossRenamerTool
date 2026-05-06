"""Maya adapter."""

import logging
import uuid

from maya import cmds

from crossrenamertool.core import constants, renamer

log = logging.getLogger(__name__)

# ! Delete before publish
import importlib

importlib.reload(renamer)
importlib.reload(constants)


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


def _process_nodes(mode, transform_function):
    """Rename nodes depending on the function.

    Args:
        mode (str): selected mode
        transform_function (callable): function(node)

    Returns:
        dict[str, str]: renamed nodes

    """
    nodes = get_nodes(mode)

    renamed = {}
    for node in nodes:

        if not cmds.objExists(node):
            log.error(f"The node {node} doesn't exist.")
            continue
        short_name = node.split("|")[-1]
        new_name = transform_function(short_name)
        if new_name and new_name != short_name:
            renamed[short_name] = _apply_rename(short_name, new_name)
        else:
            renamed[short_name] = short_name

    return renamed


def get_selection():
    """Get the current selection.

    Returns:
        list: list of selected node names

    """
    selected = cmds.ls(sl=True)
    if not selected:
        log.error("Select at least 1 node.")
        raise ValueError("No nodes selected.")
    return selected


def get_hierarchy():
    """Get selection hierarchy.

    Returns:
        list[str]: list of selected node names with hierarchy

    """
    selected = get_selection()
    transforms = (
        cmds.listRelatives(
            selected, allDescendents=True, fullPath=True, type="transform"
        )
        or []
    )
    joints = (
        cmds.listRelatives(selected, allDescendents=True, fullPath=True, type="joint")
        or []
    )
    children = list(dict.fromkeys(transforms + joints))

    return selected + children


def get_scene_objects():
    """Get all objects in the scene.

    Returns:
        list[str]: list of all node names

    """
    nodes = cmds.ls(transforms=True) or []

    return [node for node in nodes if node not in constants.DEFAULT_CAMS]


def get_nodes(mode):
    """Get the list of nodes by the selected mode.

    Args:
        mode (str): mode selected

    Returns:
        list[str]: list of nodes to renamed

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

    return nodes


def rename_nodes(mode, base_name, padding, start, step):
    """Rename nodes with padding, step and start.

    Args:
        mode (str): mode of selection
        base_name (str): base name
        padding (int): number of 0
        start (int): start number
        step (int): increment between each number

    Returns:
        dict[str, str]: renamed nodes

    """
    nodes = get_nodes(mode)

    renamed = {}
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

        if new_name and new_name != node:
            renamed[old_node] = _apply_rename(node, new_name, old_node)
        else:
            renamed[old_node] = old_node

    return renamed


def add_prefix(mode, prefix):
    """Add prefix to nodes.

    Args:
        mode (str): mode of selection
        prefix (str): prefix

    Returns:
        dict[str, str]: renamed nodes

    """
    return _process_nodes(mode, lambda node: renamer.add_prefix(node, prefix))


def add_suffix(mode, suffix):
    """Add suffix to nodes.

    Args:
        mode (str): mode of selection
        suffix (str): suffix to add

    Returns:
        dict[str, str]: renamed nodes

    """
    return _process_nodes(mode, lambda node: renamer.add_suffix(node, suffix))


def search_replace(mode, search_name, replace_name, case) -> dict[str, str]:
    """Search and replace name in node.

    Args:
        mode (str): mode of selection
        search_name (str): name to find
        replace_name (str): new name to replace
        case (bool): case sensitive

    Returns:
        dict[str, str]: renamed nodes

    """
    return _process_nodes(
        mode, lambda node: renamer.search_replace(node, search_name, replace_name, case)
    )


def add_characters(mode, text, position, from_start):
    """Add characters to a text at a specific position.

    Args:
        mode (str): mode of selection
        text (str): characters to add
        position (int): position to insert
        from_start (bool): True if insert from start else False.

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return _process_nodes(
        mode, lambda node: renamer.add_characters(node, text, position, from_start)
    )


def remove_characters(mode, position, count, from_start):
    """Delete characters at given position in the node name.

    Args:
        mode (str): mode of selection
        position (int): start index of deletion
        count (int): number of characters to delete
        from_start (bool): True count from start else from end.

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return _process_nodes(
        mode, lambda node: renamer.remove_characters(node, position, count, from_start)
    )


def text_to_lowercase(mode):
    """Convert text to lowercase.

    Args:
        mode (str): mode of selection

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return _process_nodes(mode, lambda node: renamer.text_to_lowercase(node))


def text_to_uppercase(mode):
    """Convert text to uppercase.

    Args:
        mode (str): mode of selection

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return _process_nodes(mode, lambda node: renamer.text_to_uppercase(node))


def text_to_capitalize(mode):
    """Convert text to capitalize.

    Args:
        mode (str): mode of selection

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return _process_nodes(mode, lambda node: renamer.text_to_capitalize(node))


def rename_children_from_parent(mode, padding):
    """Rename children from selected parents.

    Args:
        mode (str): mode of selection
        padding (int): number of 0

    Returns:
        dict[str, str]: renamed nodes

    """
    parents = get_nodes(mode)

    if not parents:
        return {}

    renamed = {}

    for parent in parents:
        if not cmds.objExists(parent):
            log.error(f"The node {parent} doesn't exist.")
            continue
        children = (
            cmds.listRelatives(parent, children=True, fullPath=True, type="transform")
        ) or []

        if not children:
            log.warning(f"{parent} has no children")

        temp_names = []
        for child in children:
            temp = f"__tmp_{uuid.uuid4().hex[:8]}__"
            temp_name = cmds.rename(child, temp)
            temp_names.append(temp_name)

        for temp_child, index, old_child in zip(
            temp_names, range(1, len(children) + 1), children
        ):
            new_name = renamer.renaming(parent, index, padding)
            renamed[old_child] = _apply_rename(temp_child, new_name, old_child)

    return renamed


def auto_fix_duplicates(mode, padding):
    """Auto rename duplicates nodes.

    Args:
        mode (str): mode of selection
        padding (int): number of 0

    Returns:
        dict[str, str]: renamed nodes

    """
    nodes = get_nodes(mode)

    renamed = {}

    # Rename to temp name to avoid name conflict
    node_uuids = {}
    for node in nodes:
        uuid = cmds.ls(node, uuid=True)
        if uuid:
            node_uuids[node] = uuid[0]

    for index, (node, uuid) in enumerate(node_uuids.items()):
        current_name = cmds.ls(uuid, long=True)
        if not current_name:
            log.error(f"Cannot find node with UUID {uuid}")
            continue

        current_name = current_name[0]
        parent = cmds.listRelatives(current_name, parent=True, fullPath=True)

        if parent:
            base_name = (
                current_name.replace("|", "_")
                if not current_name.startswith("|")
                else current_name.replace("|", "_")[1:]
            )

        else:
            base_name = current_name.split("|")[-1]

        new_name = renamer.renaming(base_name, index, padding)

        if new_name and new_name != current_name:
            renamed[node] = _apply_rename(current_name, new_name, node)
        else:
            renamed[node] = current_name

    return renamed


def delete_workspace_control(workspace_name: str) -> None:
    """Close and delete an existing Maya workspace control.

    Args:
        workspace_name (str): name of the workspace control to delete

    """
    if cmds.workspaceControl(workspace_name, exists=True):
        cmds.workspaceControl(workspace_name, edit=True, close=True)
        cmds.deleteUI(workspace_name, control=True)
