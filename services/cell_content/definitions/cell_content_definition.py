from abc import ABC, abstractmethod


class InvalidBucketError(Exception):
    pass


class CellContentDefinition(ABC):
    @abstractmethod
    def bucket_count(self) -> int:
        pass

    @abstractmethod
    def bucket_size(self, bucket: int) -> int:
        pass

    @abstractmethod
    def bucket_content(self, bucket: int) -> list[str]:
        pass

    @abstractmethod
    def min_bucket_size(self) -> int:
        pass

    def validate_bucket(self, bucket: int) -> None:
        min_bucket = 0
        max_bucket = self.bucket_count() - 1

        if bucket < min_bucket or bucket > max_bucket:
            raise InvalidBucketError(
                f"Bucket {bucket} is not a valid bucket."
                f" Must be between {min_bucket} and {max_bucket}."
            )
