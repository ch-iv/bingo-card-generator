import base64
from pathlib import Path


class Base64EncodeFileService:
    @staticmethod
    def call(file_path: Path) -> str:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")
