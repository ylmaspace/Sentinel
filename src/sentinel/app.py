"""Create a Qt application and database-backed main window."""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox

from sentinel.config import database_path
from sentinel.storage.database import Database
from sentinel.ui.main_window import MainWindow
from sentinel.utils.logging_config import configure_logging


def main() -> int:
    configure_logging()
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Sentinel")
    app.setOrganizationName("Sentinel")

    try:
        db = Database(database_path())
        db.initialize()
    except Exception as exc:
        QMessageBox.critical(None, "Sentinel - Startup Error", f"Local database could not be opened: {type(exc).__name__}")
        return 1

    window = MainWindow(db)
    window.show()
    return app.exec()
