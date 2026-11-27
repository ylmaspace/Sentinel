# Sentinel

Sentinel is a Windows-oriented, local-first analysis-support desktop application. It helps users inspect file identity and limited static evidence, then make informed decisions. It is not antivirus software and does not guarantee safety.

## Current status

Initial development build (0.1.0). The Qt application, local SHA-256/static identification, scan history, explicit hash-based trust registry, deterministic explanation, simulated integration/lab states, tests, and packaging templates are included. The optional VirusTotal adapter is hash-only and not enabled by the UI. No external API or installer has been tested/built as part of this source repository.

## Safety and limitations

Sentinel never executes, modifies, deletes, quarantines, blocks, or automatically uploads a selected file. It does not change Microsoft Defender, Windows security settings, or install services. Static checks are deliberately limited; no indicators does not mean safe. Digital signature verification, external AI, real reputation lookups in the interface, and behavioral sandboxing are unavailable. The lab is fictional demonstration only.

## Developer installation

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run and test

```bash
python main.py
pytest
```

The app stores SQLite data and rotating logs in the current user's local application data directory. Scan history stores the file name, hash, size, type and assessment, but not the full path or file contents. A file's name can still be personal data.

## Build executable (Windows)

```powershell
python -m pip install -e ".[dev]"
pyinstaller packaging/sentinelcore.spec
```

This produces a build artifact only when executed in a suitable Windows/PyInstaller environment. The Inno Setup configuration is a template; no finished or tested installer is included.

## Roadmap

- Reviewed, platform-native signature verification.
- Optional credential-store-backed reputation setting, explicit disclosure and tested API behavior.
- User-reviewed independent sandbox integration (not sample execution in Sentinel).
- Accessibility/localization polish and Windows release validation.

## Principles

Unknown or incomplete is not clean. Findings are evidence-labeled, and trust is a user decision rather than a safety guarantee. Sentinel supplements, never replaces, Windows security products.
