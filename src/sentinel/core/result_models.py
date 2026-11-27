"""Typed analysis and evidence models."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

class AnalysisStatus(StrEnum):
    QUEUED = "QUEUED"
    IDENTIFYING = "IDENTIFYING"
    SCANNING = "SCANNING"
    REPUTATION_CHECK = "REPUTATION_CHECK"
    ANALYSIS_INCOMPLETE = "ANALYSIS_INCOMPLETE"
    SUSPICIOUS = "SUSPICIOUS"
    DETECTED = "DETECTED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"

@dataclass(frozen=True)
class FileIdentity:
    path: str
    name: str
    size: int
    modified_at: str
    sha256: str
    detected_type: str
    extension: str
    extension_matches: bool | None

@dataclass(frozen=True)
class Evidence:
    category: str
    title: str
    detail: str
    severity: str = "info"
    source: str = "local static analysis"

@dataclass
class ScanResult:
    identity: FileIdentity
    status: AnalysisStatus
    risk: str
    evidence: list[Evidence] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    created_at: str = ""
    scan_id: int | None = None

@dataclass(frozen=True)
class ReputationResult:
    status: str
    source: str
    checked_at: str
    positives: int | None = None
    total: int | None = None
    message: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
