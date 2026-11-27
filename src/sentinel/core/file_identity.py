"""Safe file identity: metadata and SHA-256 only; never executes or writes the input."""
from __future__ import annotations

import hashlib
import mimetypes
import os
from datetime import datetime, timezone
from pathlib import Path

from sentinel.core.result_models import FileIdentity

_CHUNK_SIZE = 1024 * 1024
_MAX_HEADER_SIZE = 16


def identify_file(file_path: str | Path) -> FileIdentity:
    """Read a regular file once, calculate identity, and return bounded metadata."""
    path = Path(file_path).expanduser()
    if not path.exists():
        raise FileNotFoundError("The selected file no longer exists.")
    if not path.is_file():
        raise ValueError("The selected path is not a regular file.")

    try:
        before = path.stat()
    except (PermissionError, OSError) as exc:
        raise PermissionError("The selected file could not be inspected because it is inaccessible.") from exc

    digest = hashlib.sha256()
    header = b""
    try:
        with path.open("rb", buffering=0) as stream:
            for chunk_index, chunk in enumerate(iter(lambda: stream.read(_CHUNK_SIZE), b"")):
                if chunk_index == 0:
                    header = chunk[:_MAX_HEADER_SIZE]
                digest.update(chunk)
        after = path.stat()
    except (PermissionError, OSError) as exc:
        raise PermissionError("The selected file could not be read safely.") from exc

    if (before.st_size, before.st_mtime_ns, before.st_ino, before.st_dev) != (after.st_size, after.st_mtime_ns, after.st_ino, after.st_dev):
        raise RuntimeError("The file changed while Sentinel was calculating its identity.")

    kind = detect_type(header, path.name)
    ext = path.suffix.lower()
    expected = _expected_type(ext)
    matches = None if expected is None or kind == "Unknown / unclassified" else expected == kind

    return FileIdentity(
        str(path.resolve(strict=False)), path.name, after.st_size,
        datetime.fromtimestamp(after.st_mtime, timezone.utc).isoformat(),
        digest.hexdigest(), kind, ext, matches,
    )


def detect_type(header: bytes, filename: str = "") -> str:
    """Conservative signature/type identification from bounded input."""
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
    return {
        ".pdf": "PDF document", ".png": "PNG image", ".jpg": "JPEG image",
        ".jpeg": "JPEG image", ".gif": "GIF image", ".zip": "ZIP-compatible archive",
    }.get(extension)
