from pathlib import Path
import sqlite3
import uuid

from paths import file_identity_db_path


class FileIdentityService:
    @staticmethod
    def startup_hook():
        FileIdentityService()._ensure_db_exists()

    @staticmethod
    def lookup(key: str | None) -> Path | None:
        if key is None:
            return None

        return FileIdentityService()._lookup(key)

    @staticmethod
    def register(path: Path) -> str:
        return FileIdentityService()._register(path)

    def __init__(self):
        con = sqlite3.connect(file_identity_db_path, autocommit=True)
        self.cursor = con.cursor()

    def _ensure_db_exists(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_key TEXT UNIQUE,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def _lookup(self, key: str) -> Path | None:
        self.cursor.execute("SELECT file_path FROM files WHERE file_key = ?", (key,))
        result = self.cursor.fetchone()
        if result:
            return Path(result[0])
        return None

    def _register(self, path: Path) -> str:
        key = FileIdentityService.generate_key()
        self.cursor.execute(
            "INSERT OR IGNORE INTO files (file_key, file_path) VALUES (?, ?)",
            (key, str(path)),
        )
        return key

    @staticmethod
    def generate_key() -> str:
        return str(uuid.uuid4())
