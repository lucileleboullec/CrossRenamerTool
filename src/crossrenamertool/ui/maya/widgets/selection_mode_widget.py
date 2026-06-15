from PySide6 import QtCore, QtGui, QtWidgets


class SelectionModeBar(QtWidgets.QWidget):
    """Widget for insert and remove page."""

    MODE = {
        "Selected": "Applies the operation to the currently selected nodes only.",
        "Hierarchy": "Applies the operation to the selected nodes and all their descendants.\nShapes are excluded.",
        "Scene": "Applies the operation to all nodes in the scene.\nDefault cameras (perps, top, front, side) are excluded.",
    }

    def __init__(self, parent=None):
        """Initialize the widget."""
        super().__init__(parent=parent)

        self._configure()
        self._create_gui()

    def _configure(self):
        """Configure the widget."""
        pass

    def _create_gui(self):
        """Create the GUI."""
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.button_grp = QtWidgets.QButtonGroup()
        self.button_grp.setExclusive(True)

        for index, (mode, tooltip) in enumerate(self.MODE.items()):
            button = QtWidgets.QPushButton(mode)
            button.setCheckable(True)
            button.setFixedHeight(26)
            button.setToolTip(tooltip)
            button.setStyleSheet(self._tab_style(active=index == 0))
            self.button_grp.addButton(button, index)
            main_layout.addWidget(button)

        self.button_grp.button(0).setChecked(True)
        self.button_grp.idToggled.connect(self._on_toggle)

    def _on_toggle(self, index, checked):
        for i in range(3):
            button = self.button_grp.button(i)
            button.setStyleSheet(self._tab_style(button.isChecked()))

    def _tab_style(self, active):
        if active:
            return (
                "QPushButton { background: #e8a44a; color: #1a1a1a; border: none;"
                " padding: 4px 14px; font-size: 11px; font-weight: 600; }"
            )
        return (
            "QPushButton { background: #222222; color: #888888; border: 1px solid #3a3a3a;"
            " border-radius: 0px; padding: 4px 14px; font-size: 11px; }"
            "QPushButton:hover { background: #2e2e2e; color: #bbbbbb; }"
            "QPushButton:checked { background: #e8a44a; color: #1a1a1a; font-weight: 600; }"
        )

    @property
    def mode(self):
        modes = ["Selected", "Hierarchy", "Scene"]
        return modes[self.button_grp.checkedId()]
