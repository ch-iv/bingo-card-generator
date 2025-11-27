from abc import abstractmethod, ABC

from PIL import Image

from models.cell import Cell


class Addon(ABC):
    @abstractmethod
    def call(self, card: Image.Image, cells: list[Cell]):
        pass
