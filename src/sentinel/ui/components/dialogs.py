"""Explicit confirmation dialogs."""
from PySide6.QtWidgets import QMessageBox, QWidget

def confirm_trust(parent: QWidget, short_hash: str) -> bool:
    answer=QMessageBox.question(parent,"Add trust record",f"Trust this exact SHA-256 identity?\n{short_hash}\n\nThis is your decision, not a safety guarantee. Modified files have a different hash.",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)
    return answer == QMessageBox.StandardButton.Yes
