"""Dashboard with honest empty and status states."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from sentinel.ui.components.cards import InfoCard


class Dashboard(QWidget):
    def __init__(self, scan_count: int, trusted_count: int, on_scan) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Analysis overview")
        title.setObjectName("PageTitle")
        layout.addWidget(title)
        layout.addWidget(QLabel("SENTINEL is a local analysis-support tool. No result guarantees safety."))

        cards = QHBoxLayout()
        cards.addWidget(InfoCard("TOTAL SCANS", str(scan_count), "Locally recorded"))
        cards.addWidget(InfoCard("TRUST RECORDS", str(trusted_count), "Explicit hash-based decisions"))
        cards.addWidget(InfoCard("INTEGRATIONS", "NOT CONNECTED", "No external request configured"))
        layout.addLayout(cards)

        lab = QLabel("Lab status: SIMULATED — no file execution or behavioral analysis.")
        lab.setObjectName("Muted")
        layout.addWidget(lab)
        quick = QPushButton("Analyze a file")
        quick.clicked.connect(on_scan)
        layout.addWidget(quick)
        empty = QLabel("Recent scans appear in Reports after analysis.")
        empty.setObjectName("EmptyState")
        layout.addWidget(empty)
        layout.addStretch()
