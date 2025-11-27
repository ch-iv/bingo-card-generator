from pathlib import Path
import uuid

from PIL import Image

from models.cell import Cell
from helpers.text_in_rectangle import draw_text_in_rectangle
from .addons.addon import Addon
from .cell_content.cell_content_generator import CellContentGenerator


class FillBingoCardService:
    @staticmethod
    def call(
        unfilled_bingo_card_path: Path,
        cells: list[Cell],
        content_generator: CellContentGenerator,
        addons: list[Addon] | None = None,
    ) -> Path:
        if addons is None:
            addons = []

        return FillBingoCardService(
            unfilled_bingo_card_path, cells, content_generator, addons
        )._fill_card()

    def __init__(
        self,
        unfilled_bingo_card_path: Path,
        cells: list[Cell],
        content_generator: CellContentGenerator,
        addons: list[Addon],
    ):
        self.card = Image.open(unfilled_bingo_card_path)
        self.cells = cells
        self.content_generator = content_generator
        self.addons = addons

    @staticmethod
    def _unique_save_path() -> Path:
        directory = Path("output")
        directory.mkdir(exist_ok=True)
        return directory / f"filled_card_{uuid.uuid4()}.png"

    def _save_card(self) -> Path:
        save_path = self._unique_save_path()
        self.card.save(save_path)
        return save_path

    def _content_for_cell(self, cell: Cell) -> str:
        bucket = cell.col
        index = cell.row

        return self.content_generator.content_for(bucket, index)

    def _fill_card(self) -> Path:
        self._call_addons()

        for cell in self.cells:
            content = self._content_for_cell(cell)
            self._fill_cell(cell, content)

        return self._save_card()

    def _fill_cell(self, cell: Cell, content: str) -> None:
        if cell.row == 2 and cell.col == 2:
            return

        draw_text_in_rectangle(
            image=self.card,
            text=content,
            rect_x=cell.x1,
            rect_y=cell.y1,
            rect_width=cell.width,
            rect_height=cell.height,
            font_size=200,
            text_color="black",
        )

    def _call_addons(self) -> None:
        for addon in self.addons:
            addon.call(self.card, self.cells)
