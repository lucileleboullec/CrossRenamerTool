# Code Style Guide
All Python code in Cross Renamer Tool follows these conventions. The CI enforces them automatically via Ruff on every push.

## Formatter - Ruff format
Ruff format is the single source of truth for formatting. Never configure Black or autopep8 alongside it.

```bash
# Format all files
ruff format .

# Check without modifying
ruff format --check .
```

Key settings (from `pyproject.toml`):
```toml
[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## Imports
Imports are sorted by Ruff (isort rules, `I` ruleset) in three groups separated by a blank line:

```python
# 1. Standard  library
import json
import logging
import re
import uuid
from pathlib import Path

# 2. Third-party
from PySide6 import QtCore, QtWidgets, QtGui

# 3. First-party (crossrenamertool)
from crossrenamertool.core import constants, renamer
```

Rules:

- Never use wildcard imports (`from module import *`)  
- Never import unused modules - Ruff will flag them (`F401`)  
- Import only what you use from a module  

```python
# ❌ unused import
from PySide6 import QtCore, QtGui, QtWidgets   # QtGui unused

# ✅
from PySide6 import QtCore, QtWidgets
```

## Type hints
All public functions must have type hints on parameters and return values.

```python
# ❌ no type hints
def renaming(base_name, num, padding):
    ...

# ✅ full type hints
def renaming(base_name: str, num: int, padding: int) -> str:
    ...
```

Use `None` return type explicitly:

```python
# ✅
def _configure(self) -> None:
    self.setWindowTitle(self.TITLE)
```

## Docstrings
All public functions, methods and classes must have a Google-style docstring. Private functions (`_name`) should have one if their behavior is non-obvious.

**Function docstring**:
```python
def add_prefix(base_name: str, prefix: str) -> str:
    """Add a prefix to the node name.

    Args:
        base_name (str): base name of the node.
        prefix (str): prefix to add.

    Returns:
        str: renamed node name.

    """
    return f"{prefix}_{base_name}"
```

**Class docstring**:
```python
class AboutDialog(QtWidgets.QDialog):
    """About page with documentation and GitHub page."""
```

Rules:

- First line is a short summary - imperative mood, no trailing period
- Blank line between the summary and Args/Returns
- No space before `:` in `Args` -  `base_name (str): ...` not `base_name (str) : ...`
```python
# ❌ space before colon - griffe warning
"""
Args:
    base_name (str) : base name ← space before :
"""

# ✅
"""
Args:
    base_name (str): base name
"""
```

## Naming conventions
| Element | Convention | Example |
| --- | --- | --- |
| Module | `snake_case` | `maya_api.py` |
| Class | `PascalCase` | `RenamerWindow` |
| Function/method | `snake_case` | `add_prefix()` |
| Private function | `_snake_case` | `_apply_rename()` |
| Constant | `UPPER_SNAKE_CASE` | `DEFAULT_PADDING` |
| Variable | `snake_case` | `base_name` |
| QtSignals | `snake_case` | `request_name` |
| QtSlot (callback) | `_on_<widget>_<event>` | `_on_rename_btn_clicked()` |

## Exceptions
Never catch blind exceptions. Always catch the most specific type:
```python
# ❌ blind exception - BLE001
try:
    cmds.rename(node, new_name)
except Exception:
    log.error("rename failed")

# ✅
try:
    cmds.rename(node, new_name)
except RuntimeError as e:
    log.error(f"rename failed: {e}")
```

Always logs errors with context - never use `print()` for error reporting:
```python
# ❌
print(f"Error: {e}")

# ✅
log.error(f"Failed to rename '{node}': {e}")
```

## F-string
Use f-string for all string formatting. Never use `%` formatting or `.format()`.
```python
# ❌
log.info("Renamed '%s' to '%s'" % (old, new))
log.info("Renamed '{}' to '{}'".format(old, new))

# ✅
log.info(f"Renamed '{old}' to '{new}'")
```

Don't use f-stings without placeholders - Ruff will flag them (`F541`):
```python
# ❌ f-string without placeholder
log.warning(f"No selection")

# ✅
log.warning("No selection")
```

## Logging
Every module gets its own logger:
```python
import logging

log = logging.getLogger(__name__)
```

Use the right level:

| Level | When | 
| --- | --- | 
| `log.debug` | Internal state useful for debugging | 
| `log.info` | Normal operations - node renamed, preset saved, etc. | 
| `log.warning` | Unexpected but recoverable - no match found, node skipped | 
| `log.error` | Operation failed - node does not exist, file not found | 

## Qt-specific conventions
**Signal naming** - signals are named as requests, not events:
```python
# ❌ event-style - what happened
renamed = QtCore.Signal(str)

# ✅ request-style - what the widget is asking for
request_rename = QtSignal(str, int, int ,int)
```

**Callback naming** - slots follow `_on_<widget>_<event>`:
```python
def _on_rename_btn_clicked(self) -> None:
    ...

def _on_prefix_combo_changed(self, text: str) -> None:
    ...
```

**Layout** - always set spacing and margins explicitly:
```python
layout = QtWidgets.QVBoxLayout(self)
layout.setSpacing(8)
layout.setContentsMargins(12, 12, 12, 12)
```

## Running the linter locally
```bash
# Check all files
ruff check .

# Auto-fix what can be fixed automatically
ruff check --fix .

# Format
ruff format .

# Both in one command
ruff check --fix . && ruff format .
```

Always run this before pushing - the CI will fail if Ruff finds errors.




