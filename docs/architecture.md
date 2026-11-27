# Architecture

## Modules
- `core`: typed identity, conservative risk logic, product policy, and orchestration.
- `scanners`: read-only signature-based identification and a static evidence scanner.
- `integrations`: provider boundary, offline simulation, and a hash-only VirusTotal API adapter.
- `ai`: deterministic local explanation; external AI is disabled.
- `lab`: simulation contract only; no sample execution.
- `storage`: SQLite lifecycle and repositories for scans, trust, and non-secret settings.
- `security`: privacy defaults, input validation, and privilege boundary.
- `ui`: Qt shell, navigation, scanning worker, reports, registry, and settings.

## Data flow
A user selects a path through a file dialog. The scan worker reads metadata and file bytes only to calculate SHA-256 in chunks and inspect a small header. The static scanner adds limited signature/mismatch evidence. The risk engine derives an evidence-bounded label. The scan repository stores hash, basename, size, type, status, assessment, and evidence (not full path or content). The UI presents limitations and a deterministic explanation. Trust decisions are separately stored by exact hash and do not alter scan evidence.

## Integration boundaries
Only an explicitly configured provider can perform a reputation lookup, and the initial UI does not configure one. VirusTotal adapter sends a SHA-256 in an HTTP GET and has no file-upload method. API key is constructor-supplied; the app has no credential UI/storage. Simulation is clearly marked. Lab simulation never accesses file contents or runs a sample. Future components require explicit independent review and consent controls.
