"""Sentinel application entry point."""
from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication
from sentinel.config import database_path
from sentinel.storage.database import Database
from sentinel.ui.main_window import MainWindow
from sentinel.utils.logging_config import configure_logging

def main() -> int:
    configure_logging()
    app = QApplication(sys.argv)
    app.setApplicationName("Sentinel")
    db = Database(database_path())
    db.initialize()
    window = MainWindow(db)
    window.show()
    return app.exec()
