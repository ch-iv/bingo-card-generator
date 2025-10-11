from __future__ import annotations

import random

from .definitions.cell_content_definition import CellContentDefinition


class InvalidBucketIndexError(Exception):
    pass


class InvalidItemsPerBucketRequestedError(Exception):
    pass


class CellContentGenerator:
    def __init__(
        self, definition: CellContentDefinition, items_per_bucket: int = 5
    ) -> None:
        self.definition = definition
        self.items_per_bucket = items_per_bucket

        self._validate_items_per_bucket()

        self.content_grid = self._generate_content_grid()

    def _validate_items_per_bucket(self) -> None:
        min_items_per_bucket = 0
        # Can't generate more items than are available in the smallest bucket
        max_items_per_bucket = self.definition.min_bucket_size()

        if (
            self.items_per_bucket < min_items_per_bucket
            or self.items_per_bucket > max_items_per_bucket
        ):
            raise InvalidItemsPerBucketRequestedError(
                "Items per bucket must be between "
                "{min_items_per_bucket} and {max_items_per_bucket}. "
                "Got {self.items_per_bucket}."
            )

    def _validate_items_index(self, index: int) -> None:
        min_index = 0
        max_index = self.items_per_bucket - 1

        if index < min_index or index > max_index:
            raise InvalidBucketIndexError(
                f"Item index must be between {min_index} and {max_index}. Got {index}."
            )

    def _validate_bucket(self, bucket: int) -> None:
        self.definition.validate_bucket(bucket)

    def _generate_content_grid(self) -> list[list[str]]:
        grid: list[list[str]] = []

        for bucket in range(self.definition.bucket_count()):
            content = self.definition.bucket_content(bucket)
            chosen_content = random.sample(content, 5)
            grid.append(chosen_content)

        return grid

    def content_for(self, bucket: int, index: int) -> str:
        self._validate_bucket(bucket)
        self._validate_items_index(index)

        return self.content_grid[bucket][index]
