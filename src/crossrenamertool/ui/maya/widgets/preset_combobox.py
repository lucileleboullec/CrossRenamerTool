import logging

from PySide6 import QtCore, QtWidgets

log = logging.getLogger(__name__)


class PresetComboBox(QtWidgets.QComboBox):
    """ComboBox with right-click context menu for preset management.

    Signals:
        request_save   (str) : emitted when user wants to save current text as preset
        request_remove (str) : emitted when user wants to remove current text from presets
        request_manage ()    : emitted when user wants to open the preset manager dialog

    """

    request_save = QtCore.Signal(str)
    request_remove = QtCore.Signal(str)
    request_manage = QtCore.Signal()

    def contextMenuEvent(self, event):
        """Show context menu on right click.

        Args:
            event (QContextMenuEvent): mouse event

        """
        menu = QtWidgets.QMenu(self)

        current = self.currentText().strip()

        save_action = menu.addAction("Save as preset")
        save_action.setEnabled(bool(current))
        save_action.setToolTip("Save the current text as a reusable preset.")

        remove_action = menu.addAction("X Remove from presets")
        remove_action.setEnabled(bool(current))
        remove_action.setToolTip("Remove the selected value from the preset list.")

        menu.addSeparator()

        manage_action = menu.addAction("Manage presets...")
        manage_action.setToolTip("Open the preset manager to add, remove or reorder presets.")

        action = menu.exec(event.globalPos())

        if action == save_action:
            self.request_save.emit(current)
        elif action == remove_action:
            self.request_remove.emit(current)
        elif action == manage_action:
            self.request_manage.emit()

    def reload(self, items):
        """Reload the combobox with a new list of presets.

        Args:
            items (list[str]): new list of presets

        """
        current = self.currentText()

        self.blockSignals(True)
        self.clear()
        self.addItems(items)
        self.blockSignals(False)

        index = self.findText(current)
        self.setCurrentIndex(index if index >= 0 else -1)
        return current
