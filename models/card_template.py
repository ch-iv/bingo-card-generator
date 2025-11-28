from pathlib import Path

from paths import web_assets_path


class CardTemplate:
    def __init__(self, name: str, path: Path) -> None:
        self.name = name
        self.path = path
        self.web_safe_path = path.relative_to(web_assets_path)