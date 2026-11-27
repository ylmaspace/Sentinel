"""Application configuration and user-data paths."""
from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "Sentinel"

def user_data_dir() -> Path:
    """Return a per-user data directory without requiring elevated rights."""
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    path = root / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path

def database_path() -> Path:
    return user_data_dir() / "sentinel.sqlite3"

def log_dir() -> Path:
    path = user_data_dir() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path
