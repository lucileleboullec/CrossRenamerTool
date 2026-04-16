"""Launcher for the Cross Renamer Tool."""

from crossrenamertool import main

# ! Delete before publish
import importlib

importlib.reload(main)


def run():
    """Entry point called from Maya."""
    main.create_controller()
