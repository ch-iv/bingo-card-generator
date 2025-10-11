import pytest

from services.cell_content.definitions.american_bingo_cell_content_definition import (
    AmericanBingoCellContentDefinition,
)
from services.cell_content.definitions.cell_content_definition import InvalidBucketError


@pytest.fixture(scope="module")
def definition() -> AmericanBingoCellContentDefinition:
    return AmericanBingoCellContentDefinition()


def test_bucket_count(definition: AmericanBingoCellContentDefinition) -> None:
    assert definition.bucket_count() == 5


def test_bucket_size(definition: AmericanBingoCellContentDefinition) -> None:
    for bucket in range(0, 5):
        assert definition.bucket_size(bucket) == 15


def test_raises_error_when_requesting_size_of_negative_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    with pytest.raises(InvalidBucketError):
        definition.bucket_size(-1)


def test_raises_error_when_requesting_size_of_nonexistent_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    with pytest.raises(InvalidBucketError):
        definition.bucket_size(5)


def test_bucket_content_for_first_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    content = definition.bucket_content(0)
    expected = {
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
    }

    assert set(content) == expected


def test_bucket_content_for_last_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    content = definition.bucket_content(4)
    expected = {
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
    }

    assert set(content) == expected


def test_raises_error_when_requesting_content_of_negative_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    with pytest.raises(InvalidBucketError):
        definition.bucket_content(-1)


def test_raises_error_when_requesting_content_of_nonexistent_bucket(
    definition: AmericanBingoCellContentDefinition,
) -> None:
    with pytest.raises(InvalidBucketError):
        definition.bucket_content(5)


def test_min_bucket_size(definition: AmericanBingoCellContentDefinition) -> None:
    assert definition.min_bucket_size() == 15
