"""Main application shell and navigation."""
from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedWidget,
    QVBoxLayout, QWidget,
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

        self.setWindowTitle("SENTINEL — Analysis Support")
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
        self.nav_buttons = []

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
            self.nav_buttons.append(button)
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
        if not 0 <= index < self.stack.count():
            return
        self.stack.setCurrentIndex(index)
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
        # Refresh the dashboard and history when visited, so displayed counts/data
        # reflect the current database rather than the window's initial snapshot.
        if index == 0:
            old = self.pages[0]
            replacement = Dashboard(self.scans.count(), len(self.trust.list_all()), lambda: self.navigate(1))
            self.stack.removeWidget(old)
            old.deleteLater()
            self.pages[0] = replacement
            self.stack.insertWidget(0, replacement)
            self.stack.setCurrentIndex(0)
        elif index == 2:
            old = self.pages[2]
            replacement = ReportView(self.scans)
            self.stack.removeWidget(old)
            old.deleteLater()
            self.pages[2] = replacement
            self.stack.insertWidget(2, replacement)
            self.stack.setCurrentIndex(2)
