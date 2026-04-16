# install.py — à lancer depuis le Script Editor
from maya import cmds

# Code du bouton
button_code = """
import sys

path = r"path/to/module"
if path not in sys.path:
    sys.path.append(path)
    
from crossrenamertool.launcher import run
run()
"""

# Icône (optionnel — sinon Maya met une icône par défaut)
icon = "menuIconModify.png"  # icône native Maya

cmds.shelfButton(
    parent="Custom",  # nom de ta shelf
    label="Renamer",
    annotation="Ouvre le Maya Renamer",
    sourceType="python",
    command=button_code,
    image1=icon,
    style="iconAndTextVertical",
)

print("Shelf button installé !")
