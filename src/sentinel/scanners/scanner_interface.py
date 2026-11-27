"""Scanner plugin protocol."""
from typing import Protocol
from sentinel.core.result_models import Evidence, FileIdentity

class Scanner(Protocol):
    def scan(self, identity: FileIdentity) -> list[Evidence]: ...
