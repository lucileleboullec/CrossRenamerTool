# Create Shelf button

This guide details the steps required to create a shelf button.

1. In Maya, open the **Script Editor** (Windows> General Editors > Script Editor)  
2. Copy the code below in a Python tab.  
    ```python
    import sys

    path = r"path/to/module/src"  # update this
    if path not in sys.path:
        sys.path.append(path)

    from crossrenamertool.launcher import run
    run()
    ```
3. Selection the code.  
4. RMB > Save Script to Shelf...  
5. Name it : `Cross Renamer Tool`.  
6. Cross Renamer Tool button is inside your shelf !  