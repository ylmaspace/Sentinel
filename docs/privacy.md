# Privacy

Sentinel is local-first. SQLite history stores a file's SHA-256, basename, byte size, detected type, result and evidence; it intentionally omits the absolute path and raw file contents. Logs rotate under the user's local app-data directory and should not include full paths or secrets. The basename/hash may still be sensitive.

No network operation occurs by default. The optional VirusTotal adapter, when explicitly constructed with an API key and invoked, sends the SHA-256 hash to VirusTotal over HTTPS; it does not upload the file. The API key is not stored by the initial GUI. Provider terms, rate limits, privacy implications and authorization must be reviewed before enabling it. Reputation responses are untrusted and may be incomplete. Simulated mode is offline and fictional.

External AI and file upload are disabled. Future external analysis must explain what is transmitted and obtain explicit consent before sending any hash, content or private document. Users can remove local database/log files themselves; the application currently has no data-retention UI.
