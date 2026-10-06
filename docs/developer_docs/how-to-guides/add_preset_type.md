# Add a preset type
Use this guide when you want to add a new category of presets beyond prefixes and suffixes - for example a preset list for side indicators or node type suffixes.

## Step 1 - Add the JSON file
Create a new file in `src/crossrenamertool/resources/presets/`:
```json
// src/crossrenamertool/resources/presets/sides.json

{
    "presets": ["L", "R", "C", "M"]
}
```

## Step 2 - Register the path in `presets.py`
```python
# src/crossrenamertool/core/presets.py

SIDES_PATH = PRESETS_DIR / "sides.json"

_PATHS = {
    "prefixes": PREFIXES_PATH,
    "suffixes": SUFFIXES_PATH, 
    "sides": SIDES_PATH, # ← add here
}
```
The unified API (`load_presets`,`save_presets`, `add_preset`, `remove_preset`) works automatically for any key registered in `_PATHS` - no other changes needed in `presets.py`.

## Step 3 - Add the default values in `constants.py`
```python
# src/crossrenamertool/core/constants.py

SIDES = ["L", "R", "C", "M"] # ← add here
```
This is used by the Reset to Default action in `PresetsDialog`.

## Step 4 - Update `PresetsDialog._on_reset`
```Python
# src/crossrenamertool/ui/[DCC]/widgets/presets_dialog.py

def _on_reset(self) -> None:
    ...
    presets_manager.save_presets("prefixes", constants.PREFIXES)
    presets_manager.save_presets("suffixes", constants.SUFFIXES)
    presets_manager.save_presets("sides", constants.SIDES)
    self._load()
```

## Step 5 - Use the new preset type in the UI
Whenever you need the preset list in a combobox:
```python
from crossrenamertool.core import presets ad presets_manager

self.sides_combo = PresetComboBox()
self.sides_combo.preset_type = "sides"
self.sides_combo.addItems(presets_manager.load_presets("sides"))
self.sides_combo.setEditable(True)
self.sides_combo.setCurrentIndex(-1)
```