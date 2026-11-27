"""Read-only platform signature-check abstraction; not implemented yet."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SignatureStatus:
    available: bool
    verified: bool | None
    message: str

def verify_signature(_path: str) -> SignatureStatus:
    """No platform trust API is wired in; do not imply a verification occurred."""
    return SignatureStatus(False, None, "Digital signature verification is unavailable in this build.")
