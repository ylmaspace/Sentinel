"""Small parameterized settings repository. Secrets must not be stored here."""
from sentinel.storage.database import Database

class SettingsRepository:
    def __init__(self, database: Database) -> None: self.database = database
    def get(self, key: str, default: str = "") -> str:
        with self.database.connect() as db:
            row=db.execute("SELECT value FROM settings WHERE key=?",(key,)).fetchone()
            return str(row[0]) if row else default
    def set(self, key: str, value: str) -> None:
        if "key" in key.lower() or "token" in key.lower() or "secret" in key.lower(): raise ValueError("Credentials must use an OS credential store, not application settings.")
        with self.database.connect() as db: db.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(key,value))
