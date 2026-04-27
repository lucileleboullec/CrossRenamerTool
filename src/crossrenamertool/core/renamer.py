import logging
import re

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
    if not base_name or not num or not padding:
        log.warning("You have to write the new name with configuration")
        return None

    return f"{base_name.capitalize()}_{num:0{padding}d}"


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


def search_replace(node, search_name, replace_name):
    """Search and replace name in node.

    Args:
        node (str): node selected
        search_name (str): name to find
        replace_name (str): new name to replace

    Returns:
        str: new name renamed

    """
    if not re.search(re.escape(search_name), node, flags=re.IGNORECASE):
        return node
    return re.sub(re.escape(search_name), replace_name, node, flags=re.IGNORECASE)
