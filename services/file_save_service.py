from pathlib import Path

from werkzeug.datastructures import FileStorage

from .file_identity_service import FileIdentityService
from paths import file_save_path


class ErrorSavingFile(Exception):
    pass


class FileSaveService:
    @staticmethod
    def call(
        file: FileStorage, file_name: str, save_location: Path = file_save_path
    ) -> str:
        if not file:
            raise ErrorSavingFile("No file provided")

        if file_name == "":
            raise ErrorSavingFile("File can't be empty")

        file_path = file_save_path / file_name

        file.save(file_path)

        return FileIdentityService.register(file_path)
