"""Application settings and safety information."""
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsView(QWidget):
    """Honest settings placeholder; no system or security settings are changed."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Settings & information")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        sections = (
            ("Application", "SENTINEL — local file analysis support."),
            ("Privacy", "File contents are not uploaded or executed. Scan history stores file identity metadata and evidence, not the full file path."),
            ("Limitations", "Static inspection cannot establish safety. No signature verification, behavioral sandbox, or live reputation integration is active in this interface."),
            ("Trust registry", "Trust records apply only to an exact SHA-256 identity. They do not suppress analysis and are not a safety guarantee."),
            ("System impact", "SENTINEL does not change Windows security settings, install services, or perform automatic file actions."),
            ("Configuration", "No configurable system-security controls are provided in this build."),
        )
        for heading, description in sections:
            label = QLabel(f"{heading}\n{description}")
            label.setWordWrap(True)
            label.setObjectName("Muted")
            layout.addWidget(label)
        layout.addStretch()
