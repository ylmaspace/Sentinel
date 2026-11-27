"""Validation helpers for user-controlled inputs."""
import re

def validate_sha256(value: str) -> str:
    normalized=value.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", normalized): raise ValueError("Expected a 64-character SHA-256 hash.")
    return normalized
