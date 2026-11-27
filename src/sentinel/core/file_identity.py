"""Safe file identity: metadata and SHA-256 only; never executes or writes the input."""
from __future__ import annotations
import hashlib
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from sentinel.core.result_models import FileIdentity

_CHUNK_SIZE = 1024 * 1024

def identify_file(file_path: str | Path) -> FileIdentity:
    """Identify a regular file and hash it incrementally; errors are raised to caller."""
    path = Path(file_path).expanduser()
    stat = path.stat()
    if not path.is_file():
        raise ValueError("The selected path is not a regular file.")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(_CHUNK_SIZE):
            digest.update(chunk)
    with path.open("rb") as stream:
        header = stream.read(16)
    kind = detect_type(header, path.name)
    ext = path.suffix.lower()
    expected = _expected_type(ext)
    matches = None if expected is None or kind == "Unknown / unclassified" else expected == kind
    return FileIdentity(str(path.resolve()), path.name, stat.st_size,
        datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(), digest.hexdigest(), kind, ext, matches)

def detect_type(header: bytes, filename: str = "") -> str:
    """Return a conservative type from file signatures, not the filename alone."""
    if header.startswith(b"MZ"):
        return "Windows executable (PE header; signature not verified)"
    if header.startswith(b"%PDF-"):
        return "PDF document"
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG image"
    if header.startswith(b"PK\x03\x04"):
        return "ZIP-compatible archive"
    if header.startswith(b"\x7fELF"):
        return "ELF executable"
    if header[:3] == b"\xff\xd8\xff":
        return "JPEG image"
    if header.startswith((b"GIF87a", b"GIF89a")):
        return "GIF image"
    if not header:
        return "Empty file"
    try:
        header.decode("utf-8")
        return "Text (UTF-8-compatible prefix)"
    except UnicodeDecodeError:
        mime, _ = mimetypes.guess_type(filename)
        return f"Binary data ({mime})" if mime else "Unknown / unclassified"

def _expected_type(extension: str) -> str | None:
    mapping = {".pdf": "PDF document", ".png": "PNG image", ".jpg": "JPEG image", ".jpeg": "JPEG image", ".gif": "GIF image", ".zip": "ZIP-compatible archive"}
    return mapping.get(extension)
