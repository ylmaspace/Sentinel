# Repository guidance for Copilot

- Preserve the modular boundaries in `src/sentinel`; keep business logic out of widgets.
- Sentinel is analysis support, not antivirus. Never add automatic execution, deletion, quarantine, modification, blocking, upload, trust, persistence, elevation, or Defender/security-setting changes.
- Unknown, unavailable, conflicting, and incomplete evidence must not become a clean verdict. Never present absence of indicators as a safety guarantee.
- Read selected files only; do not execute samples. Use harmless temporary files in deterministic tests.
- Use typed models, parameterized SQL, explicit error handling, and minimal dependency additions.
- Never commit API keys, log secrets, file contents, or unnecessary absolute paths. Hash lookups require explicit opt-in and transmission disclosure.
- Keep external AI disabled unless explicit consent and privacy handling are implemented. Keep the laboratory simulated until an independently reviewed sandbox exists.
- Run `pytest` after changes and document untested platform-specific behavior. Do not claim a package/installer has been built unless it has actually been built and tested.
