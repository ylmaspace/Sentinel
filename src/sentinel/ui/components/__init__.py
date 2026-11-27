"""Local settings and integration availability."""
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel
from sentinel.security.privacy import PRIVACY_NOTICE

class SettingsView(QWidget):
    def __init__(self) -> None:
        super().__init__(); layout=QVBoxLayout(self); title=QLabel("Settings"); title.setObjectName("PageTitle"); layout.addWidget(title)
        layout.addWidget(QLabel("External reputation: SIMULATED by default. No network request is made."))
        layout.addWidget(QLabel("VirusTotal hash-only adapter exists in code but is not configured by this interface. API credentials are not stored by Sentinel."))
        layout.addWidget(QLabel(PRIVACY_NOTICE)); layout.addWidget(QLabel("Signature verification and external AI are unavailable. File upload is disabled.")); layout.addStretch()
