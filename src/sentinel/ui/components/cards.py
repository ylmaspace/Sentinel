"""Card building blocks."""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

class InfoCard(QFrame):
    def __init__(self, title: str, value: str, detail: str = "") -> None:
        super().__init__(); self.setObjectName("InfoCard")
        layout=QVBoxLayout(self); heading=QLabel(title); heading.setObjectName("CardHeading")
        self.value=QLabel(value); self.value.setObjectName("CardValue"); self.detail=QLabel(detail); self.detail.setObjectName("Muted")
        layout.addWidget(heading); layout.addWidget(self.value); layout.addWidget(self.detail)
