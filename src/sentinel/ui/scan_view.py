"""File selection and background-safe scan display."""
from __future__ import annotations
import logging
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QFileDialog,QProgressBar,QTextEdit
from sentinel.core.orchestrator import Orchestrator
from sentinel.storage.scan_repository import ScanRepository
from sentinel.ai.report_explainer import explain
from sentinel.utils.file_utils import format_size

class ScanWorker(QThread):
    completed=Signal(object); failed=Signal(str)
    def __init__(self,path: str, repository: ScanRepository) -> None: super().__init__(); self.path=path; self.repository=repository
    def run(self) -> None:
        try: self.completed.emit(Orchestrator(self.repository).analyze(self.path))
        except Exception as exc:
            logging.getLogger(__name__).exception("File analysis failed")
            self.failed.emit(f"Analysis could not be completed ({type(exc).__name__}). Check that the file is accessible.")

class ScanView(QWidget):
    def __init__(self, repository: ScanRepository) -> None:
        super().__init__(); self.repository=repository; self.selected_path=""; self.worker=None
        layout=QVBoxLayout(self); title=QLabel("File scanner"); title.setObjectName("PageTitle"); layout.addWidget(title)
        layout.addWidget(QLabel("Files are read for identification only. Sentinel never executes, modifies, deletes, quarantines or uploads them."))
        actions=QHBoxLayout(); self.pick=QPushButton("Choose file…"); self.pick.clicked.connect(self.choose_file); self.start=QPushButton("Start local analysis"); self.start.setEnabled(False); self.start.clicked.connect(self.start_scan); actions.addWidget(self.pick); actions.addWidget(self.start); layout.addLayout(actions)
        self.progress=QProgressBar(); self.progress.setRange(0,1); self.progress.setValue(0); layout.addWidget(self.progress)
        self.output=QTextEdit(); self.output.setReadOnly(True); self.output.setPlaceholderText("Choose a file to see its identity, then run static analysis."); layout.addWidget(self.output)
    def choose_file(self) -> None:
        path,_=QFileDialog.getOpenFileName(self,"Select a file")
        if path: self.selected_path=path; self.output.setPlainText(f"Selected: {path}\nReady for local analysis."); self.start.setEnabled(True)
    def start_scan(self) -> None:
        if not self.selected_path: return
        self.start.setEnabled(False); self.pick.setEnabled(False); self.progress.setRange(0,0); self.output.setPlainText("IDENTIFYING → SCANNING\nCalculating SHA-256 and inspecting limited file metadata…")
        self.worker=ScanWorker(self.selected_path,self.repository); self.worker.completed.connect(self.show_result); self.worker.failed.connect(self.show_error); self.worker.finished.connect(self.finished); self.worker.start()
    def finished(self) -> None:
        self.progress.setRange(0,1); self.progress.setValue(1); self.pick.setEnabled(True); self.start.setEnabled(bool(self.selected_path))
    def show_error(self,message: str) -> None: self.output.setPlainText("ANALYSIS_INCOMPLETE\n"+message)
    def show_result(self,result) -> None:
        identity=result.identity
        lines=[f"Status: {result.status.value}",f"Assessment: {result.risk}",f"Name: {identity.name}",f"Size: {format_size(identity.size)}",f"Detected type: {identity.detected_type}",f"Last modified (UTC): {identity.modified_at}",f"SHA-256: {identity.sha256}","", "Evidence:"]
        lines.extend(f"• {item.title}: {item.detail}" for item in result.evidence)
        lines.extend(["", "Limitations:", *[f"• {item}" for item in result.limitations], "", "Deterministic explanation:", explain(result)])
        self.output.setPlainText("\n".join(lines))
