"""Hash-based trust registry controls."""
from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from sentinel.storage.trust_repository import TrustRepository
from sentinel.ui.components.dialogs import confirm_trust


class TrustView(QWidget):
    def __init__(self, repository: TrustRepository) -> None:
        super().__init__()
        self.repository = repository

        layout = QVBoxLayout(self)
        title = QLabel("Trust registry")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        layout.addWidget(QLabel("Trust applies only to the exact SHA-256. It does not guarantee safety or bypass subsequent analysis."))

        actions = QHBoxLayout()
        add = QPushButton("Add hash…")
        add.clicked.connect(self.add_hash)
        revoke = QPushButton("Revoke selected")
        revoke.clicked.connect(self.revoke)
        actions.addWidget(add)
        actions.addWidget(revoke)
        layout.addLayout(actions)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["SHA-256", "Decision date (UTC)", "Note"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        self.refresh()

    def refresh(self) -> None:
        try:
            rows = self.repository.list_all()
        except Exception as exc:
            QMessageBox.critical(self, "Trust registry error", f"The trust registry could not be read: {type(exc).__name__}")
            return
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column, key in enumerate(("sha256", "created_at", "note")):
                self.table.setItem(row_index, column, QTableWidgetItem(str(row[key])))

    def add_hash(self) -> None:
        value, ok = QInputDialog.getText(self, "Add trust record", "SHA-256:", QLineEdit.EchoMode.Normal)
        if not ok:
            return
        try:
            if confirm_trust(self, value.strip()):
                self.repository.add(value.strip())
                self.refresh()
        except ValueError as exc:
            QMessageBox.warning(self, "Invalid hash", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Trust registry error", f"The trust record could not be saved: {type(exc).__name__}")

    def revoke(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            return
        item = self.table.item(row, 0)
        if item is None:
            return
        answer = QMessageBox.question(self, "Revoke trust", "Revoke trust for this exact SHA-256?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            if self.repository.revoke(item.text().strip()):
                self.refresh()
        except Exception as exc:
            QMessageBox.critical(self, "Trust registry error", f"The trust record could not be revoked: {type(exc).__name__}")
