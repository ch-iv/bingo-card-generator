from services.cell_content.definitions.cell_content_definition import (
    CellContentDefinition,
)


class AmericanBingoCellContentDefinition(CellContentDefinition):
    def bucket_count(self) -> int:
        return 5

    def bucket_size(self, bucket: int) -> int:
        self.validate_bucket(bucket)

        return 15

    def min_bucket_size(self) -> int:
        return 15

    def bucket_content(self, bucket: int) -> list[str]:
        self.validate_bucket(bucket)

        size = self.bucket_size(bucket)

        start = bucket * size + 1
        end = start + size

        return [str(i) for i in range(start, end)]
