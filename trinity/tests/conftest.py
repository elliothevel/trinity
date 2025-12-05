import csv
import os
import typing

import pytest


DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data',
)



@pytest.fixture
def read_data() -> typing.Callable[[str], list[dict[str, str]]]:
    """A fixture for reading test data."""
    def _read_data(filename: str) -> list[dict[str, str]]:
        """Read test data."""
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath) as fp:
            reader = csv.DictReader(fp)
            return list(reader)

    return _read_data
