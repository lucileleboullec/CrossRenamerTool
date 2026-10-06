# Add a rename operation

Use this guide whenever you want to add a new renaming operation to the tool - for example a new convert case mode, a new search pattern, or any string transformation.

## The pattern - 4 file to touch
Every operation follows the same path through the MVC stack:
```code
renamer.py → [dcc]_api.py → main.py → [widget].py + main_window.py
```

## Step 1 - Add the pure function in `renamer.py`
The function takes a `str` and returns a `str`. No DCC, no UI.

```python
def my_operation(node: str, param: str) -> str:
    """Short description

    Args:
        node (str): node name
        param (str): operation parameter

    Returns:
        str: transformed node name
    
    """
    # your logic here
    return node
```

## Step 2 - Add the adapter in `[DCC]_api.py`
If your functions fits the `_process_nodes` pattern (one node in, one name out):
```python
def my_operation(mode: str, param: str) -> dict[str, str]:
    """Short description

    Args:
        mode (str): mode of selection
        param (str): operation parameter

    Returns:
        dict[str, str]: renamed nodes
    
    """
    return _process_nodes(mode, lambda node: renamer.my_operation(node, param))
```

If it needs special handling (batch, two-pass, UUID), implement your own loop. See `rename_nodes` or `auto_fix_duplicates` as examples.

## Step 3 - Add the controller method in `main.py`

```python
def my_operation(self, mode: str, param: str) -> dict[str, str]:
    """Short description

    Args:
        mode (str): mode of selection
        param (str): operation parameter

    Returns:
        dict[str, str]: renamed nodes
    
    """
    return [DCC]_api.my_operation(mode, param)
```

## Step 4 - Add the signal and button in the relevant widget
Add a signal to the widget class:

```python
request_my_operation = QtCore.Signal(str) # pass param as str
```

Add the button and connect it:
```python
my_btn = QtWidgets.QPushButton("My Operation")
my_btn.clicked.connect(self.my_operation)
layout.addWidget(my_btn)

def _on_my_operation(self) -> None:
    param = self.my_field.text()
    self.request_my_operation.emit(param)
```

## Step 5 - Connect the signal in `main_window.py`
```python
# In _create_gui
self.my_page.request_my_operation.connect(self.my_operation)

# Handler method
def my_operation(self, param: str) -> None:
    mode = self.get_current_mode()
    self.controller.my_operation(mode, param)
```

## Step 6 - Write the test
```python
# tests/test_renamer.py
class TestMyOperation(unittest.TestCase):
    
    def test_basic(self):
        self.assertEqual(renamer.my_operation("arm_L", "param"), "expected_result")

    def test_empty(self):
        self.assertEqual(renamer.my_operation("", "param"), "")
```