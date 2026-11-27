"""Small, read-only static checks with strictly evidence-backed findings."""
from sentinel.core.result_models import Evidence, FileIdentity

class StaticScanner:
    def scan(self, identity: FileIdentity) -> list[Evidence]:
        findings: list[Evidence] = [Evidence("identity", "SHA-256 calculated", identity.sha256, "info")]
        if identity.extension_matches is False:
            findings.append(Evidence("type", "Extension and detected type differ", f"Extension {identity.extension or '(none)'} does not match detected signature: {identity.detected_type}.", "medium"))
        if identity.detected_type.startswith("Windows executable"):
            findings.append(Evidence("type", "Executable file signature observed", "The file begins with an MZ header. This identifies a common executable format but does not indicate maliciousness.", "info"))
        return findings
