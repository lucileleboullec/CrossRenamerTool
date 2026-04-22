import logging

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
    if not prefix:
        log.warning("Can't add prefix to your name.")

    return f"{prefix}_{base_name}"
