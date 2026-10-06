# Write tests
Cross Renamer Tool uses `unittest` for all unit tests. Tests run without a DCC session - only `renamer.py` and `presets.py` are tested directly.

## File structure
```code
tests/
    test_renamer.py  ← tests for core/renamer.py
    test_presets.py  ← tests for core/presets.py
```

## Basic test structure
```python
import unittest
from crossrenamertool.core import renamer

class TestAddPrefix(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(renamer.add_prefix("arm_L", "CTRL"), "CTRL_arm_L")

    def test_empty_prefix(self):
        self.assertIsNone(renamer.add_prefix("arm_L", ""))

    def test_empty_base_name(self):
        self.assertIsNone(renamer.add_prefix("", "CTRL"))

    def test_already_has_prefix(self):
        result = renamer.add_prefix("CTRL_arm_L", "CTRL")
        self.assertEqual(result, "CTRL_CTRL_arm_L")

if __name__ == "__main__":
    unittest.main()
```

## What to test
For every function in `renamer.py`, test:

| Case | Example | 
| --- | --- |
| Normal use | `add_prefix("arm_L", "CTRL")` → `"CTRL_arm_L"` |
| Empty input | `add_prefix("", "CTRL")` → `None` | 
| Edge case | `remove_characters("arm", 0, 999, True)` → no crash |
| No match |  `search_replace("arm_L", "leg", "arm", True)` → unchanged | 
| Both directions | `swap_side("arm_L", ...)` and `swap_side("arm_R", ...)` |

## Testing presets with a temporary file
Presets read and write to JSON files. Use `tmp_path` via `unittest.mock` to avoid touching the real presets:

```python
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from crossrenamertool.core import presets as presets_manager

class TestPresets(unittest.TestCase):

    def setUp(self):
        import tempfile
        self.tmp_dir = tempfile.mkdtemp()
        self.tmp_path = Path(self.tmp_dir) / "prefixes.json"
        self.tmp_path.write_text(json.dumps({"presets": ["CTRL", "JNT"]}))
        
        self.patcher = patch.dict(presets_manager._PATHS, {"prefixes": self.tmp_path})
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_load_presets(self):
        result = presets_manager.load_presets("prefixes")
        self.assertEqual(result, ["CTRL", "JNT"])

    def test_add_preset(self):
        presets_manager.add_preset("prefixes", "FK")
        result = presets_manager.load_presets("prefixes")
        self.assertIn("FK", result)

    def test_no_duplicate(self):
        presets_manager.add_preset("prefixes", "CTRL")   # already exists
        result = presets_manager.load_presets("prefixes")
        self.assertEqual(result.count("CTRL"), 1)
```

## Running the tests
```bash
# Set up the environment
$env:PYTHONPATH = "src" 

# Run all tests
python -m unittest discover -s tests -v

# Run a specific file
python -m unittest discover -s tests -p "test_renaming.py" -v

# Run a specific class
python -m unittest tests.test_cross_renamer_tool.test_renaming.TestSwapSide -v

# Run a specific test
python -m unittest tests.test_cross_renamer_tool.test_renaming.TestSwapSide.test_suffix_L -v
```

## Common assertions

| Assertion | Use case | 
| --- | --- | 
| `assertEqual(a, b)` | Two values are equal | 
| `assertIsNone(x)` | Value is None |
| `assertIsNotNone(x)` | Value is not None | 
| `assertIn(item, container)` | Item is in a list or string | 
| `assertNotIn(item, container)` | Item is not in a list |
| `assertRaises(Error, func, *args)` | Function raises an exception | 

## What NOT to test
- Maya `cmds` calls - these require a running Maya session and belong to integration tests
- Qt widget rendering - test the logic, not the UI
- Private functions (`_apply_rename`, `_process_nodes`) - test them indirectly through the public API