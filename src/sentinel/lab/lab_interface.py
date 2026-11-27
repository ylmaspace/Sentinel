"""Behavioral analysis interface. Implementations must be independently reviewed."""
from typing import Protocol

class Lab(Protocol):
    def evaluate(self, sha256: str) -> dict[str, str]: ...
