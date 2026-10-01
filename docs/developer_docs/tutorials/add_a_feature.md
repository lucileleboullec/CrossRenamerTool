# Add a feature end to end

This tutorial walks through adding a complete renaming feature to Cross Renamer Tool - from the pure logic in `renamer.py` to the UI button. We will add a `text_to_lowercase` conversion as a concrete example.

**Prerequisites**: [Set up the development environment](../setup_dev_environment/)

## 1. Create a feature branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/text_to_lowercase
```

## 2. Add the pure logic in `renamer.py`

The first layer is always the pure function - no DCC, no UI.

```Python
# src/crossrenamertool/core/renamer.py

def text_to_lowercase(node: str) -> str:
    """Change node name to lowercase.

    Args:
        node (str): node

    Returns:
        str: renamed node

    """
    return node.lower()
```

## 3. Write the test
Before touching DCC, write a unit test:
```python
# tests/ test_renamer.py

class TestConvertCase(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(renamer.text_to_lowercase("CTRL_ARM_L"), "ctrl_arm_l")

    def test_already_correct(self):
        self.assertEqual(renamer.text_to_lowercase("ctrl_arm_l"), "ctrl_arm_l")
```

Run the tests:
```bash
$env:PYTHONPATH = "src"  
python -m unittest discover -s tests -v
```
All tests must pass before moving to the next step.

## 4. Add the DCC adapter in `[dcc]_api.py`

```python
# src/crossrenamertool/model/maya_api.py

def text_to_lowercase(mode) -> dict[str, str]:
    """Convert text to lowercase.

    Args:
        mode (str): mode of selection

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return _process_nodes(mode, lambda node: renamer.text_to_lowercase(node))
```
Because `text_to_lowercase` takes a string and returns a string, `_process_nodes` handles everything - node retrieval, existence check, rename, log.

# 5. Add the controller method in `main.py`
```python
# src/crossrenamertool/main.py

def text_to_lowercase(self, mode: str) -> dict[str, str]:
    """Convert text to lowercase.

    Args:
        mode (str): mode of selection

    Returns:
        dict[str, str]: dictionary of nodes

    """
    return maya_api.text_to_lowercase(mode)
```

## 6. Add the UI button in `case_widget.py`
```python
# src/crossrenamertool/ui/maya/widgets/case_widget.py

class CasePage(QtWidgets.QWidget):
    """Widget for case sensitive page."""

    TITLE = "Case"

    request_lowercase = QtCore.Signal() # ← new signal
    request_uppercase = QtCore.Signal()
    request_capitalize = QtCore.Signal()
    request_title = QtCore.Signal()
    request_camel = QtCore.Signal()
    request_pascal = QtCore.Signal()
    request_snake = QtCore.Signal()

    def __init__(self, parent=None) -> None:
        """Initialize the widget."""
        super().__init__(parent=parent)

        self._configure()
        self._create_gui()

    def _configure(self) -> None:
        """Configure the widget."""
        self.setWindowTitle(self.TITLE)

    def _create_gui(self) -> None:
        """Create the GUI."""
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        # ...

        cases = [
            ("lowercase", "all lowercase", self._on_lowercase), # ← new button
            ("UPPERCASE", "ALL UPPERCASE", self._on_uppercase),
            ("Title", "First Letter Of Each Word", self._on_title),
            ("Capitalize", "First letter only", self._on_capitalize),
            ("camelCase", "camelCase (split on _ and -)", self._on_camel),
            ("PascalCase", "PascalCase (split on _ and -)", self._on_pascal),
            ("snake_case", "snake_case (split on uppercase)", self._on_snake),
        ]

        # ...

    def _on_lowercase(self) -> None:
        """Convert text to lowercase."""
        self.request_lowercase.emit()

    # ...
```

## 7. Connect the signal in `main_window.py`

```python
# src/crossrenamertool/ui/maya/main_window.py

# In _create_gui, connect the new signal
self.case_page.request_lowercase.connect(self.text_to_lowercase)

# Add the handler method
def text_to_lowercase(self):
    """Convert text to lowercase."""
    self.controller.text_to_lowercase(self.mode_bar.mode)
```

## 8. Run the full check
```bash
# Lint
ruff check .

# Tests
python -m unittest discover -s tests -v
```
Both must pass before committing.

## 9. Commit and push
```bash
git add .
git commit -m "✨(renamer): Add text to lowercase conversion"
git push origin feature/text-to-lowercase
```

## 10. Open a Pull Request
On GitHub, open PR from `feature/text-to-lowercase` into `develop` with: 
- **Title**: `✨(renamer): Add text to lowercase conversion`
- **Description**: what was added, how to test it, screenshots of the new button

The CI will run lint → tests → docs automatically. The PR can be merged once all checks are green.