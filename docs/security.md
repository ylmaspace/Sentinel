# Security

## Threat model and principles
Sentinel processes user-selected files as untrusted data. The initial workflow opens files read-only, hashes incrementally, examines only a short header, and never executes or changes a sample. It uses standard dialogs, parameterized SQLite queries, no shell commands, and no administrator privileges. Findings are evidence-based; missing, conflicting, or unavailable information is not clean. No automatic trust, deletion, quarantine, blocking, Defender changes, service installation, or persistence is allowed.

## Limitations and risks
Static identification is not malware detection. File formats can be malformed; Python/Qt and OS parsers may have vulnerabilities. Very large files may consume time and I/O. A hash lookup discloses a stable identifier and external services can return stale/incomplete/untrusted results. Scan metadata and filenames can be sensitive. The first release lacks signature validation, sandboxing, credential-store integration, and formal security review. Sentinel must not replace Microsoft Defender or other protections.

## Safe development
Use harmless temporary files in tests; never execute samples. Keep unknown statuses unknown. Add no automatic file actions, upload, elevated privilege, persistence, security-tool changes, or shell execution. Treat all API data as untrusted; do not log secrets or file content. Validate inputs and use parameterized SQL. External integrations remain opt-in with disclosure and explicit consent. Independently review any future sandbox implementation.
