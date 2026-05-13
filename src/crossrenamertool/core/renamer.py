import logging
import re
from crossrenamertool.core import constants

log = logging.getLogger(__name__)


def renaming(base_name, num, padding) -> str:
    """Create the new name for the node.

    Args:
        base_name (str): base name of the node.
        num (int): number for the padding.
        padding (int): number of 0 for padding.

    Returns:
        str: new name for the node.

    """
    if not base_name:
        log.warning("base_name is empty.")
        return None
    if num is None or padding is None:
        log.warning("Num or Padding is None.")
        return None

    return f"{base_name}_{num:0{padding}d}"


def add_prefix(base_name, prefix) -> str:
    """Add prefix to the node.

    Args:
        base_name (str): base name
        prefix (str): prefix

    Returns:
        str: renamed name

    """
    if not base_name:
        log.warning("You don't have any base name on the node.")
        return None
    if not prefix:
        log.warning("Can't add prefix to your name.")
        return None

    return f"{prefix}_{base_name}"


def add_suffix(base_name, suffix):
    """Add suffix to the node.

    Args:
        base_name (str): base name
        suffix (str): suffix to add

    Returns:
        str: renamed name

    """
    if not base_name:
        log.warning("You don't have any base name on the node.")
        return None

    if not suffix:
        log.warning("Can't add suffix to your name.")
        return None

    return f"{base_name}_{suffix}"


def search_replace(node, search_name, replace_name, case):
    """Search and replace name in node.

    Args:
        node (str): node selected
        search_name (str): name to find
        replace_name (str): new name to replace
        case (bool): case sensitive

    Returns:
        str: new name renamed

    """
    flags = 0 if case else re.IGNORECASE

    if not re.search(re.escape(search_name), node, flags=re.IGNORECASE):
        return node
    return re.sub(re.escape(search_name), replace_name, node, flags=flags)


def add_characters(node, text, position, from_start):
    """Insert text at a given position in the node name.

    Args:
        node (str): node name
        text (str): text to insert
        position (int): index position
        from_start (bool): True, count from start. False, from end

    Returns:
        str: new node name

    """
    index = position if from_start else -position or len(node)
    return node[:index] + text + node[index:]


def remove_characters(node, position, count, from_start):
    """Delete characters at given position in the node name.

    Args:
        node (str): node name
        position (int): start index of deletion
        count (int): number of characters to delete
        from_start (bool): True count from start else from end.

    Returns:
        str: new node name

    """
    if count >= len(node):
        log.warning("Can't delete all characters.")
        return node
    index = position if from_start else len(node) - position - count
    index = max(0, min(index, len(node)))
    count = max(0, min(count, len(node) - index))

    return node[:index] + node[index + count :]


def text_to_lowercase(node):
    """Change node name to lowercase.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    return node.lower()


def text_to_uppercase(node):
    """Change node name to uppercase.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    return node.upper()


def text_to_capitalize(node):
    """Change node name to capitalize.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    return node.capitalize()


def swap_side(node, swap_sides):
    """Swap side indicator in the node.

    Args:
        node (str): selected node
        swap_sides (dict[str, str]): dictionary of the sides

    Returns:
        str: new name with swap side

    """
    if not swap_sides:
        log.error("The swap_sides dictionary wasn't found")
        return None

    for left, right in swap_sides.items():
        pattern = rf"(?<![a-zA-Z])({left}|{right})(?![a-zA-Z])"

        match = re.search(pattern, node)

        if not match:
            continue

        side = match.group(1)
        opposite = right if side == left else left
        return re.sub(pattern, opposite, node, count=1)

    log.warning(f"No side indicator found in '{node}'")
    return None
