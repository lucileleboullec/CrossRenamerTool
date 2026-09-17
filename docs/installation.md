# Installation

## Requires
- Autodesk Maya 2026+
- Blender 5.0+
- Python 3.10+
- PySide6 (bundled with Maya 2025+; install separately for Maya 2024)

## Launch

### Option 1 - Scripts folder
1. Clone or download the repository into your Maya scripts folder:
```
# Windows
C:/Users/<you>/Documents/maya/scripts/

# macOS / Linux
~/maya/scripts/
```

2. Open the **Scripts Editor** in Maya, create a **Python** tab and paste:
```python
from crossrenamertool import launcher
lancher.run()
```
!!! tip 
    Create a shelf button for launch the tool quickly. If you want to save the tool in a shelf, follow [[How To Guide] Create Shelf Button](user_manual/how-to-guides/guides/create_shelf_button.md)

### Options 2 - `userSetup.py`
Add the following code to your `userSetup.py` file (located in your Maya scripts folder):
```python
# userSetup.py
import maya.utils as utils

def launch_cross_renamer():
    from crossrenamertool import launcher
    launcher.run()

utils.executeDeferred(launch_cross_renamer)
```
!!! note
    `executeDeferred`  ensures Maya has fully loaded its UI before the tool launches

### Options 3 - `install.py` script
1. Open the **Scripts Editor** in Maya, create a **Python** tab.
2. Paste the following code and update the `paste` variable with the path to the `src` folder on your machine:
```python
# install.py — to execute into the script editor
from maya import cmds

# Button code
button_code = """
import sys

path = r"path/to/module/src"  # update this
if path not in sys.path:
    sys.path.append(path)

from crossrenamertool.launcher import run
run()
"""

# Icon
icon = "menuIconModify.png"

cmds.shelfButton(
    parent="Custom",
    label="Renamer",
    annotation="Open Cross Renamer Tool",
    sourceType="python",
    command=button_code,
    image1=icon,
    style="iconAndTextVertical",
)

print("Shelf button installed !")
```
3. Execute the script by pressing **Ctrl+Enter** or clicking the **Execute** button.

4. A **Renamer** button will appear in your **Custom** shelf.

!!! tip
    The `Custom` shelf must already exist in Maya. If it doesn't, create it first via **Shelf Editor → New Shelf**.
