# install.py — à lancer depuis le Script Editor
from maya import cmds

# Code du bouton
button_code = """
import sys

path = r"path/to/module/src"
if path not in sys.path:
    sys.path.append(path)

from crossrenamertool.launcher import run
run()
"""

# Icône (optionnel — sinon Maya met une icône par défaut)
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

print("Shelf button installé !")
