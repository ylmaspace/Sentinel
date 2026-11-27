"""Hash-based trust registry controls."""
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QPushButton,QInputDialog,QLineEdit,QMessageBox
from sentinel.storage.trust_repository import TrustRepository
from sentinel.ui.components.dialogs import confirm_trust

class TrustView(QWidget):
    def __init__(self,repository: TrustRepository) -> None:
        super().__init__(); self.repository=repository; layout=QVBoxLayout(self); title=QLabel("Trust registry"); title.setObjectName("PageTitle"); layout.addWidget(title)
        layout.addWidget(QLabel("Trust applies only to the exact SHA-256. It does not guarantee safety or bypass subsequent analysis."))
        actions=QHBoxLayout(); add=QPushButton("Add hash…"); add.clicked.connect(self.add_hash); revoke=QPushButton("Revoke selected"); revoke.clicked.connect(self.revoke); actions.addWidget(add); actions.addWidget(revoke); layout.addLayout(actions)
        self.table=QTableWidget(0,3); self.table.setHorizontalHeaderLabels(["SHA-256","Decision date (UTC)","Note"]); self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); self.table.horizontalHeader().setStretchLastSection(True); layout.addWidget(self.table); self.refresh()
    def refresh(self) -> None:
        rows=self.repository.list_all(); self.table.setRowCount(len(rows))
        for r,row in enumerate(rows):
            for c,key in enumerate(("sha256","created_at","note")): self.table.setItem(r,c,QTableWidgetItem(row[key]))
    def add_hash(self) -> None:
        value,ok=QInputDialog.getText(self,"Add trust record","SHA-256:",QLineEdit.EchoMode.Normal)
        if not ok:return
        try:
            if confirm_trust(self,value): self.repository.add(value); self.refresh()
        except ValueError as exc: QMessageBox.warning(self,"Invalid hash",str(exc))
    def revoke(self) -> None:
        row=self.table.currentRow()
        if row<0:return
        item=self.table.item(row,0)
        if item and self.repository.revoke(item.text()):self.refresh()
