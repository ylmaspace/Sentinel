"""Hash-only VirusTotal API adapter. Never uploads files."""
from __future__ import annotations
from datetime import datetime, timezone
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from sentinel.core.result_models import ReputationResult

class VirusTotalClient:
    BASE_URL = "https://www.virustotal.com/api/v3/files/"
    def __init__(self, api_key: str | None = None, timeout: float = 8.0) -> None:
        self.api_key, self.timeout = api_key, timeout
    def lookup_hash(self, sha256: str) -> ReputationResult:
        now = datetime.now(timezone.utc).isoformat()
        if not self.api_key:
            return ReputationResult("UNAVAILABLE", "VirusTotal", now, message="API key is not configured; no request made.")
        if len(sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha256):
            return ReputationResult("ERROR", "VirusTotal", now, message="Invalid SHA-256 value.")
        request = Request(self.BASE_URL + sha256.lower(), headers={"x-apikey": self.api_key, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read(1_000_000))
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            positives, total = int(stats.get("malicious", 0)) + int(stats.get("suspicious", 0)), sum(int(v) for v in stats.values() if isinstance(v, int))
            status = "AVAILABLE" if total else "UNKNOWN"
            return ReputationResult(status, "VirusTotal", now, positives, total, "Hash lookup only; external service response is untrusted.", data)
        except HTTPError as exc:
            status = "UNKNOWN" if exc.code == 404 else "UNAVAILABLE"
            return ReputationResult(status, "VirusTotal", now, message=f"Lookup unavailable (HTTP {exc.code}); not a clean result.")
        except (URLError, TimeoutError, ValueError, OSError) as exc:
            return ReputationResult("UNAVAILABLE", "VirusTotal", now, message=f"Lookup failed ({type(exc).__name__}); not a clean result.")
