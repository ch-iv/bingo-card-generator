import random
from pathlib import Path

from PIL import Image

from services.addons.addon import Addon
from models.cell import Cell


class WarmAndFuzzyAddon(Addon):
    def __init__(
        self,
        red_path: Path,
        blue_path: Path,
    ):
        self.red_path = red_path
        self.blue_path = blue_path

    def call(
        self,
        image: Image.Image,
        cells: list[Cell],
    ) -> None:
        cells_copy = cells[:]
        cells_copy = list(filter(lambda cell: cell.row != 2 or cell.col != 2, cells_copy))
        chosen_cells = random.sample(cells_copy, 2)

        red_image = Image.open(self.red_path).convert("RGBA")
        blue_image = Image.open(self.blue_path).convert("RGBA")

        first_top_left = chosen_cells[0].top_left()
        second_top_left = chosen_cells[1].top_left()
        delta_x = 2
        delta_y = 2

        image.paste(blue_image, (first_top_left[0] + delta_x, first_top_left[1] + delta_y), blue_image)
        image.paste(red_image, (second_top_left[0] + delta_x, second_top_left[1] + delta_y), red_image)
