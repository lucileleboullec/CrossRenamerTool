"""Presets manager for prefixes and suffixes."""

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

PRESETS_DIR = Path(__file__).parent.parent / "resources" / "presets"
PREFIXES_PATH = PRESETS_DIR / "prefixes.json"
SUFFIXES_PATH = PRESETS_DIR / "suffixes.json"

_PATHS = {
    "prefixes": PREFIXES_PATH,
    "suffixes": SUFFIXES_PATH,
}


def _get_path(preset_type: str) -> Path:
    """Get the JSON path for a given preset type.

    Args:
        preset_type (str): "prefixes" or "suffixes"

    Returns:
        Path: path to the JSON file

    Raises:
        ValueError: if preset_type is unknown

    """
    path = _PATHS.get(preset_type)
    if path is None:
        raise ValueError(f"Unknown preset type: '{preset_type}'. Expected: {list(_PATHS)}")
    return path


def _load(path: Path) -> list:
    """Load presets from JSON file.

    Args:
        path (Path): path to the JSON file

    Returns:
        list[str]: list of presets

    """
    if not path.exists():
        log.warning(f"Presets file not found : {path}")
        return []

    with open(path) as f:
        data = json.load(f)

    return data.get("presets", [])


def _save(path: Path, presets: list):
    """Save presets to a JSON file.

    Args:
        path (Path): path to the JSON file
        presets (_type_): list of presets to save

    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump({"presets": presets}, f, indent=4)

    log.info(f"Presets save to {path}")


def load_presets(preset_type: str):
    """Load presets.

    Args:
        preset_type (str): "prefixes" or "suffixes"

    Returns:
        list[str]: list of presets

    """
    return _load(_get_path(preset_type))


def save_presets(preset_type: str, presets: list) -> None:
    """Save presets for a given type.

    Args:
        preset_type (str)      : "prefixes" or "suffixes"
        presets     (list[str]): list of presets to save

    """
    _save(_get_path(preset_type), presets)


def add_preset(preset_type: str, value: str) -> list:
    """Add a value to the presets of a given type.

    Args:
        preset_type (str): "prefixes" or "suffixes"
        value       (str): value to add

    Returns:
        list[str]: updated list of presets

    """
    presets = load_presets(preset_type)

    if value in presets:
        log.warning(f"'{value}' already exists in {preset_type}.")
        return presets

    presets.append(value)
    save_presets(preset_type, presets)
    return presets


def remove_preset(preset_type: str, value: str) -> list:
    """Remove a value from the presets of a given type.

    Args:
        preset_type (str): "prefixes" or "suffixes"
        value       (str): value to remove

    Returns:
        list[str]: updated list of presets

    """
    presets = load_presets(preset_type)

    if value not in presets:
        log.warning(f"'{value}' not found in {preset_type}.")
        return presets

    presets.remove(value)
    save_presets(preset_type, presets)
    return presets


def save_prefixes(presets: list) -> None:
    save_presets("prefixes", presets)


def save_suffixes(presets: list) -> None:
    save_presets("suffixes", presets)


def add_prefixes(prefix: str) -> list:
    add_preset("prefixes", prefix)


def add_suffixes(suffix: str) -> list:
    add_preset("suffixes", suffix)


def remove_prefixes(prefix: str) -> list:
    remove_preset("prefixes", prefix)


def remove_suffixes(suffix: str) -> list:
    remove_preset("suffixes", suffix)
