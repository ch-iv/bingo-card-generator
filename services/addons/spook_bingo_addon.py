import random
from pathlib import Path

from PIL import Image

from services.addons.addon import Addon
from models.cell import Cell


class SpookBingoAddon(Addon):
    def __init__(
        self,
        four_to_win_image_path: Path,
        no_columns_image_path: Path,
        no_rows_image_path: Path,
    ):
        self.four_to_win_image_path = four_to_win_image_path
        self.no_columns_image_path = no_columns_image_path
        self.no_rows_image_path = no_rows_image_path

    def call(
        self,
        image: Image.Image,
        cells: list[Cell],
    ) -> None:
        trick_image_path = random.sample(
            [self.no_columns_image_path, self.no_rows_image_path], 1
        )[0]
        cells_copy = cells[:]
        cells_copy = list(filter(lambda cell: cell.row != 2 or cell.col != 2, cells_copy))
        chosen_cells = random.sample(cells_copy, 2)

        four_to_win_image = Image.open(self.four_to_win_image_path).convert("RGBA")
        trick_image = Image.open(trick_image_path).convert("RGBA")
        first_top_left = chosen_cells[0].top_left()
        second_top_left = chosen_cells[1].top_left()
        delta_x = 2
        delta_y = 2
        image.paste(four_to_win_image, (first_top_left[0] + delta_x, first_top_left[1] + delta_y), four_to_win_image)
        image.paste(trick_image, (second_top_left[0] + delta_x, second_top_left[1] + delta_y), trick_image)
