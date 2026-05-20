from PySide6 import QtWidgets, QtCore


class AboutDialog(QtWidgets.QDialog):
    DOC_URL = "https://github.com/your-org/maya-renamer/wiki"
    GIT_URL = "https://github.com/your-org/maya-renamer"

    TITLE = "About Maya Renamer"

    def __init__(self, parent=None, stylesheet=""):
        super().__init__(parent)

        self.stylesheet = stylesheet

        self._configure()
        self._create_gui()

    def _configure(self):
        """Configure the widget."""
        self.setWindowTitle(self.TITLE)
        if self.stylesheet:
            self.setStyleSheet(self.stylesheet)
        self.setFixedSize(420, 300)

    def _create_gui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        title = QtWidgets.QLabel("Maya Node Renamer")
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #e8a44a;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title)

        version = QtWidgets.QLabel("v1.0.0  ·  PySide6  ·  Maya 2024+")
        version.setStyleSheet("color: #666666; font-size: 11px;")
        version.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(version)

        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.HLine)
        sep.setStyleSheet("color: #3a3a3a;")
        main_layout.addWidget(sep)

        desc = QtWidgets.QLabel(
            "A comprehensive renaming utility for Autodesk Maya.\n"
            "Batch rename, prefix/suffix, search & replace,\n"
            "insert/remove, case conversion, and utilities."
        )
        desc.setAlignment(QtCore.Qt.AlignCenter)
        desc.setStyleSheet("color: #aaaaaa; font-size: 11px; line-height: 1.5;")
        main_layout.addWidget(desc)

        main_layout.addStretch()

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(8)

        doc_btn = QtWidgets.QPushButton("  Documentation")
        doc_btn.setObjectName("primary")
        doc_btn.setFixedHeight(32)
        # doc_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.DOC_URL)))
        btn_row.addWidget(doc_btn)

        git_btn = QtWidgets.QPushButton("  GitHub")
        git_btn.setFixedHeight(32)
        git_btn.setStyleSheet(
            "QPushButton { background: #24292e; color: #d4d4d4; border: 1px solid #444;"
            " border-radius: 4px; padding: 5px 12px; }"
            "QPushButton:hover { background: #2f363d; }"
        )
        # git_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.GIT_URL)))
        btn_row.addWidget(git_btn)

        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setFixedHeight(32)
        close_btn.setFixedWidth(70)
        close_btn.clicked.connect(self.close)
        btn_row.addWidget(close_btn)

        main_layout.addLayout(btn_row)
