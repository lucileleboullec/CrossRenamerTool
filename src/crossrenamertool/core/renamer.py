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
        return f"{base_name}"

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


def remove_prefix(node, prefix):
    """Remove prefix in the name.

    Args:
        node (str): node name
        prefix (str): prefix to remove

    Returns:
        str: new name

    """
    if node.startswith(prefix):
        return node[len(prefix) :]

    return node


def remove_suffix(node, suffix):
    """Remove suffix in the name.

    Args:
        node (str): node name
        suffix (str): suffix to remove

    Returns:
        str: new name

    """
    if node.endswith(suffix):
        return node[: -len(suffix)]

    return node


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

    return re.sub(search_name, replace_name, node, flags=flags)


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


def text_to_title(node):
    """Change node name to title.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    return node.title()


def text_to_camel(node):
    """Change node name to camel.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    parts = re.split(r"[_\-\s]+", node)

    return parts[0].lower() + "".join(part.capitalize() for part in parts[1:])


def text_to_pascal(node):
    """Change node name to pascal.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    parts = re.split(r"[_\-\s]+", node)

    return "".join(part.capitalize() for part in parts)


def text_to_snake(node):
    """Change node name to snake.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    node = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", node)
    node = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", node)

    return node.lower()


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

    all_sides = "|".join(re.escape(side) for side in swap_sides)
    pattern = rf"(?<![a-zA-Z])({all_sides})(?![a-zA-Z])"
    match = re.search(pattern, node)

    if not match:
        log.warning(f"No side indicator found in '{node}'")
        return node

    side = match.group(1)
    opposite = swap_sides.get(side)
    if not opposite:
        log.warning(f"No opposite found for '{side}'")
        return node

    return re.sub(pattern, opposite, node, count=1)


def fix_shape_name(transform_name, shape_index):
    """Generate the correct shape name from its transform name.

    Args:
        transform_name (str) : name of the transform node
        shape_index (int) : index for multiple shapes (0 = no number)

    Returns:
        str: correct shape name

    """
    if shape_index == 0:
        return f"{transform_name}Shape"

    return f"{transform_name}Shape_{shape_index:03d}"
