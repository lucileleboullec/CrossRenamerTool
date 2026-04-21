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
    if not base_name:
        log.warning("You have to write the new name")

    return f"{base_name}_{num:0{padding}d}"
