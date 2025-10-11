import pytest

from services.cell_content.cell_content_generator import (
    CellContentGenerator,
    InvalidBucketIndexError,
    InvalidItemsPerBucketRequestedError,
)
from services.cell_content.definitions.american_bingo_cell_content_definition import (
    AmericanBingoCellContentDefinition,
)
from services.cell_content.definitions.american_bingo_cell_content_definition import (
    CellContentDefinition,
)

from services.cell_content.definitions.cell_content_definition import InvalidBucketError


@pytest.fixture(scope="module")
def definition() -> AmericanBingoCellContentDefinition:
    return AmericanBingoCellContentDefinition()


@pytest.fixture(scope="module")
def generator(definition: CellContentDefinition) -> CellContentGenerator:
    return CellContentGenerator(
        AmericanBingoCellContentDefinition(), items_per_bucket=5
    )


def test_initializes_with_valid_items_per_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    generator = CellContentGenerator(definition, items_per_bucket=5)
    assert generator.items_per_bucket == 5


def test_raises_error_when_items_per_bucket_is_negative(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    with pytest.raises(InvalidItemsPerBucketRequestedError):
        CellContentGenerator(definition, items_per_bucket=-1)


def test_raises_error_when_items_per_bucket_exceeds_minimum_bucket_size(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    with pytest.raises(InvalidItemsPerBucketRequestedError):
        CellContentGenerator(definition, items_per_bucket=16)


def test_content_for_returns_items_from_first_bucket(
    generator: CellContentGenerator,
) -> None:
    for index in range(5):
        content = generator.content_for(bucket=0, index=index)
        assert content in generator.definition.bucket_content(0)


def test_content_for_returns_items_from_last_bucket(
    generator: CellContentGenerator,
) -> None:
    for index in range(5):
        content = generator.content_for(bucket=4, index=index)
        assert content in generator.definition.bucket_content(4)


def test_content_for_raises_error_for_negative_bucket(
    generator: CellContentGenerator,
) -> None:
    with pytest.raises(InvalidBucketError):
        generator.content_for(bucket=-1, index=0)


def test_content_for_raises_error_for_nonexistent_bucket(
    generator: CellContentGenerator,
) -> None:
    with pytest.raises(InvalidBucketError):
        generator.content_for(bucket=5, index=0)


def test_content_for_raises_error_for_negative_index(
    generator: CellContentGenerator,
) -> None:
    with pytest.raises(InvalidBucketIndexError):
        generator.content_for(bucket=0, index=-1)


def test_content_for_raises_error_for_index_out_of_range(
    generator: CellContentGenerator,
) -> None:
    with pytest.raises(InvalidBucketIndexError):
        generator.content_for(bucket=0, index=5)
