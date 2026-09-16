# CrossRenamerTool

## Overview
The **Cross Renamer Tool** is a production-ready renaming utility for Autodesk Maya and Blender. It covers the full range of renaming operations an artist needs on a daily basis.

> [!IMPORTANT]  
> For now, the tool only works in Autodesk Maya

## Documentation
You can find the documentation at this [link]()

## Requires
- Autodesk Maya (2024+)
- Blender 5.0
- Optional: `unittest`

## Launch
In maya script editor :
```
import sys

path = r"path/to/module"
if path not in sys.path:
    sys.path.append(path)
    
from crossrenamertool.launcher import run
run()
```
> [!NOTE]  
> Replace the path with the actual path to your `CrossRenamerTool/src` directory

## Contribute
Developed by **Lucile Le Boullec** - Junior TD/Rigger - le.boullec.lucile@gmail.com




