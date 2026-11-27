"""Main application shell and navigation."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from sentinel.storage.database import Database
from sentinel.storage.scan_repository import ScanRepository
from sentinel.storage.trust_repository import TrustRepository
from sentinel.ui.dashboard import Dashboard
from sentinel.ui.report_view import ReportView
from sentinel.ui.scan_view import ScanView
from sentinel.ui.settings_view import SettingsView
from sentinel.ui.trust_view import TrustView


class MainWindow(QMainWindow):
    """Owns the desktop shell and its repository dependencies."""

    def __init__(self, database: Database) -> None:
        super().__init__()
        self.database = database
        self.scans = ScanRepository(database)
        self.trust = TrustRepository(database)

        self.setWindowTitle("Sentinel - Analysis Support")
        self.resize(1120, 760)
        self.setMinimumSize(820, 580)

        style = Path(__file__).parent / "styles" / "theme.qss"
        if style.is_file():
            self.setStyleSheet(style.read_text(encoding="utf-8"))

        root = QWidget()
        outer = QVBoxLayout(root)

        header = QLabel("SENTINEL  /  FILE ANALYSIS SUPPORT")
        header.setObjectName("Header")
        outer.addWidget(header)

        body = QHBoxLayout()
        sidebar = QVBoxLayout()
        self.stack = QStackedWidget()

        self.pages = [
            Dashboard(self.scans.count(), len(self.trust.list_all()), lambda: self.navigate(1)),
            ScanView(self.scans),
            ReportView(self.scans),
            TrustView(self.trust),
            SettingsView(),
        ]

        labels = ["Dashboard", "File Scanner", "Reports", "Trust Registry", "Settings"]
        for index, (label, page) in enumerate(zip(labels, self.pages)):
            button = QPushButton(label)
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, i=index: self.navigate(i))
            sidebar.addWidget(button)
            self.stack.addWidget(page)

        sidebar.addStretch()
        body.addLayout(sidebar, 1)
        body.addWidget(self.stack, 5)
        outer.addLayout(body, 1)

        footer = QLabel("Analysis support only  •  Unknown is not clean  •  No automatic file actions")
        footer.setObjectName("Footer")
        outer.addWidget(footer)

        self.setCentralWidget(root)
        self.navigate(0)

    def navigate(self, index: int) -> None:
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
