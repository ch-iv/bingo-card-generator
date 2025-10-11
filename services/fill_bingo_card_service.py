from pathlib import Path
import uuid

from PIL import Image

from ..models.cell import Cell
from ..helpers.text_in_rectangle import draw_text_in_rectangle


class FillBingoCardService:
    @staticmethod
    def call(
        unfilled_bingo_card_path: Path, cells: list[Cell], texts: list[list[str]]
    ) -> Path:
        return FillBingoCardService(unfilled_bingo_card_path, cells, texts)._fill_card()

    def __init__(
        self, unfilled_bingo_card_path: Path, cells: list[Cell], texts: list[list[str]]
    ):
        self.card = Image.open(unfilled_bingo_card_path)
        self.cells = cells
        self.texts = texts

    @staticmethod
    def _unique_save_path() -> Path:
        return Path(__file__).parent / "output" / f"filled_card_{uuid.uuid4()}.png"

    def _save_card(self) -> Path:
        save_path = self._unique_save_path()
        self.card.save(save_path)
        return save_path

    def _fill_card(self) -> Path:
        for cell in self.cells:
            content = self.texts[cell.row][cell.col]
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
            font_size=92,
            text_color="black",
        )
