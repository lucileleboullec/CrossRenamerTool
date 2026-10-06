# Add a UI page
Use this guide when you want to add a new tab page to the `QStackedWidget` in `MainWindow`.

## Step 1 - Create the widget file
Create the new file in `src/crossrenamertool/ui/[DCC]/widgets/`:
```python
# src/crossrenamertool/ui/[DCC]/widgets/my_page_widget.py

from PySide6 import QtCore, QtWidgets

class MyPage(QtWidget.QWidget):
    """Widget for my new page."""

    TITLE = "My Page"

    # Declare signals for every action the page an request
    request_my_action = QtCore.Signal(str)

    def __init__(self, parent=None) -> None:
        """Initialize the widget."""
        super().__init__(parent=parent)
        self._configure()
        self._create_gui()

    def _configure(self) -> None:
        """Configure the widget."""
        self.setWindowTitle(self.TITLE)

    def _create_gui(self):
        """Create the GUI."""
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # Add your widget here
        self.my_field = QtWidgets.QLineEdit()
        self.my_field.setPlaceholderText("Input...")
        main_layout.addWidget(self.my_field)

        my_btn = QtWidgets.QPushButton("Apply")
        my_btn.clicked.connect(self._on_apply)
        main_layout.addWidget(my_btn)

        main_layout.addStretch()

    def _on_apply(self) -> None:
        """Emit the action signal."""
        value = self.my_field.text().strip()
        if not value:
            return
        self.request_my_action.emit(value)
```

## Step 2 - Register the page in `MainWindow`
```python
# src/crossrenamertool/ui/[DCC]/main_window.py

# 1. Import the new widget
from crossrenamertool.ui.[DCC].widgets import my_page_widget

# 2. Add the page label to PAGES
class MainWindow(...):
    PAGES = [
        "Rename",
        "Prefix/Suffix",
        "Search/Replace",
        "Insert/Remove",
        "Convert Case",
        "Utils",
        "My Page",    # ← add here
    ]

# 3. Instantiate the page in __init__
def __init__(self, controller, parent=None):
    ...
    self.my_page = my_page_widget.MyPage()

# 4. Add to the QStackedWidget in _create_gui
self.stack.addWidget(self.my_page)

# 5. Connect the signal
self.my_page.request_my_action.connect(self.my_action)

# 6. Add the handler method
def my_action(self, value: str) -> None:
    """Handle my action."""
    mode = self.get_current_mode()
    self.controller.my_action(mode, value)
```

## Step 3 - Add the controller method
```python
# src/crossrenamertool/main.py

def my_action(self, mode: str, value: str) -> dict[str, str]:
    """My action.

    Args:
        mode (str): mode of selection
        value (str): action parameter

    Returns:
        dict[str, str]: renamed nodes

    """
    return [DCC]_api.my_action(mode, value)
```

