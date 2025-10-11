from pathlib import Path

import pytest

from services.detect_image_cells_service import DetectImageCellsService
from models.cell import Cell


@pytest.fixture(scope="module")
def cells() -> list[Cell]:
    template_path = Path(__file__).parent / "fixtures" / "bingo_card_template.png"
    return DetectImageCellsService.call(template_path)


def test_correct_number_of_cells(cells: list[Cell]) -> None:
    assert len(cells) == 25  # 5x5 grid


def test_output_contains_all_unique_columns(cells: list[Cell]) -> None:
    columns = {cell.col for cell in cells}
    assert columns == {0, 1, 2, 3, 4}


def test_output_contains_all_unique_rows(cells: list[Cell]) -> None:
    rows = {cell.row for cell in cells}
    assert rows == {0, 1, 2, 3, 4}
