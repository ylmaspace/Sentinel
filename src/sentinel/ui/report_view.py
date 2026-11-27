"""Scan history view."""
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem
from sentinel.storage.scan_repository import ScanRepository

class ReportView(QWidget):
    def __init__(self, repository: ScanRepository) -> None:
        super().__init__(); layout=QVBoxLayout(self); title=QLabel("Reports & history"); title.setObjectName("PageTitle"); layout.addWidget(title)
        layout.addWidget(QLabel("Historical evidence is preserved independently of trust decisions."))
        rows=repository.recent(); table=QTableWidget(len(rows),5); table.setHorizontalHeaderLabels(["When (UTC)","Name","SHA-256","Status","Assessment"]); table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        for r,row in enumerate(rows):
            values=[row["created_at"],row["name"],row["sha256"],row["status"],row["risk"]]
            for c,value in enumerate(values): table.setItem(r,c,QTableWidgetItem(str(value)))
        table.horizontalHeader().setStretchLastSection(True); layout.addWidget(table)
