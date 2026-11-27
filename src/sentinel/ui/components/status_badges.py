"""Status display labels."""
from PySide6.QtWidgets import QLabel

class StatusBadge(QLabel):
    def __init__(self, status: str) -> None:
        super().__init__(status); self.setObjectName("StatusBadge"); self.setToolTip("Status describes Sentinel's analysis workflow, not a guarantee of file safety.")
